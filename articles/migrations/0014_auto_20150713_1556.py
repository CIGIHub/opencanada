# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_articlepage_style'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlepage',
            old_name='style',
            new_name='feature_style',
        ),
    ]
