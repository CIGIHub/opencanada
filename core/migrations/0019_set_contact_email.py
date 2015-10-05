# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_email(apps, schema_editor):

    SiteDefaults = apps.get_model('core', 'SiteDefaults')
    defaults = SiteDefaults.objects.all()

    for default_settings in defaults:
        default_settings.contact_email = "info@opencanada.org"
        default_settings.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20151002_2248'),
    ]

    operations = [
        migrations.RunPython(set_email),
    ]
