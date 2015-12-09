# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0083_auto_20151208_2156'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StaticJsonDataContent',
        ),
        migrations.RemoveField(
            model_name='articlepage',
            name='static_json',
        ),
    ]
