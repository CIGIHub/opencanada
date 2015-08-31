# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0048_articlepage_interview'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlelistpage',
            name='filter_for_interviews',
            field=models.BooleanField(default=False),
        ),
    ]
