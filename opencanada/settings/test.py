from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WP_IMPORTER_IMAGE_DOWNLOAD_DOMAINS = ("www.example.com", "example.com", "placekitten.com", )
WP_IMPORTER_USER_PHOTO_URL_PATTERN = "http://placekitten.com/g/50/{}"
