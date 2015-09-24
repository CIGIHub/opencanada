from django.conf import settings


def settings_context(request):
    return {'GOOGLE_ANALYTICS_PROPERTY_ID': settings.GOOGLE_ANALYTICS_PROPERTY_ID,
            'IS_PRODUCTION': settings.IS_PRODUCTION,
            'ADMIN_ENABLED': settings.ADMIN_ENABLED,
            }
