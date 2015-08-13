# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0033_articlepage_last_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlepage',
            old_name='last_updated',
            new_name='cached_last_updated',
        ),
    ]
