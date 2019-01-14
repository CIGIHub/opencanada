#!/usr/bin/env python
import os
import sys
import warnings

import dotenv

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    dotenv.read_dotenv()

if __name__ == "__main__":
    if os.environ.get('OPEN_CANADA_PYTHON_ENV') == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opencanada.settings.production')
    elif os.environ.get('OPEN_CANADA_PYTHON_ENV') == 'staging':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opencanada.settings.staging')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opencanada.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
