from __future__ import absolute_import, division, unicode_literals

import httplib2
import os
import six

from analytics.models import Analytics
from apiclient.discovery import build
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from oauth2client.service_account import ServiceAccountCredentials


def get_creds_path():
    message = 'Setting ANALYTICS_CREDS_PATH must be defined, exist and be a directory.'
    try:
        path = getattr(settings, 'ANALYTICS_CREDS_PATH')
    except AttributeError:
        raise ImproperlyConfigured(message)

    if not os.path.isdir(path):
        raise ImproperlyConfigured(message)

    return path


def get_service_account_email():
    message = 'Setting ANALYTICS_SERVICE_ACCOUNT_EMAIL must be defined and non empty'
    try:
        email = getattr(settings, 'ANALYTICS_SERVICE_ACCOUNT_EMAIL')
    except AttributeError:
        raise ImproperlyConfigured(message)

    if email is None or email == '':
        raise ImproperlyConfigured(message)

    return email


def get_key_file_location():
    creds_path = get_creds_path()
    key_file_location = os.path.join(creds_path, 'open-canada-analytics.p12')

    if not os.path.isfile(key_file_location):
        raise ImproperlyConfigured(
            '{} must be a file which contains your api key.'.format(key_file_location)
        )

    return key_file_location


def get_service(api_name, api_version, scopes, key_file_location, service_account_email):
    """Get a service that communicates to a Google API.

    Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

    Returns:
    A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        service_account_email,
        key_file_location,
        scopes=scopes
    )

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if not accounts.get('items'):
        return None

    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
        accountId=account
    ).execute()

    if not properties.get('items'):
        return None

    # Get the first property id.
    property = properties.get('items')[0].get('id')

    # Get a list of all views (profiles) for the first property.
    profiles = service.management().profiles().list(
        accountId=account,
        webPropertyId=property
    ).execute()

    if not profiles.get('items'):
        return None

    # return the first view (profile) id.
    return profiles.get('items')[0].get('id')


def reset_analytics(pages):
    '''
    Set existing analytics to 0.
    '''
    for url, page in six.iteritems(pages):
        analytics = get_analytics(page)
        analytics.last_period_views = 0
        analytics.save()


def get_analytics(page):
    '''
    Ensure the analytics row exists for a given page
    '''
    analytics, _ = Analytics.objects.get_or_create(page=page)
    return analytics
