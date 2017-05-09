# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_themes(apps, schema_editor):
    pass  # refactored with grey jay and theme no longer needs to be set.


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_set_contact_email'),
        ('themes', '0003_auto_20170502_1814'),
    ]

    operations = [
        migrations.RunPython(set_themes),
    ]
