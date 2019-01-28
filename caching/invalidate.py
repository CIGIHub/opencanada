from __future__ import absolute_import, unicode_literals

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_cloudflare_config = None


def get_cloudflare_config():
    global _cloudflare_config
    if _cloudflare_config is None:
        config = getattr(settings, 'WAGTAILFRONTENDCACHE', None)
        if config is None:
            logger.error('Configuration Error: WAGTAILFRONTENDCACHE expected in settings. Cache not invalidated.')
            return None

        if 'cloudflare' not in config:
            logger.error('Configuration Error: Key "cloudflare" expected in WAGTAILFRONTENDCACHE setting. Cache not invalidated.')
            return None

        _cloudflare_config = config['cloudflare']

    return _cloudflare_config


def cloudflare_request(method, url, data):
    cloudflare_config = get_cloudflare_config()

    if cloudflare_config is None:
        return

    url_base = 'https://api.cloudflare.com/client/v4'
    url = url_base + url.format(**cloudflare_config)

    headers = {
        'X-Auth-Email': cloudflare_config['EMAIL'],
        'X-Auth-Key': cloudflare_config['TOKEN'],
    }

    resp = method(url, json=data, headers=headers)

    try:
        resp_json = resp.json()
    except ValueError:
        logger.error('Cloudflare API Error: Unable to parse response into JSON. {}'.format(resp.content))
        return None


    logger(resp_json)
    if resp_json['success'] is False:
        logger.error('Cloudflare API Error: Request did not succeed. {}'.format(resp_json))
        return None

    return resp


def cloudflare_purge_all():
    data = {"purge_everything": True}

    cloudflare_request(
        requests.delete,
        '/zones/{ZONEID}/purge_cache',
        data,
    )
