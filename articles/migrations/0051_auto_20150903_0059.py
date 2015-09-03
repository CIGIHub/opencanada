# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0050_auto_20150901_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='sticky_for_type_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='externalarticlepage',
            name='sticky_for_type_section',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='sticky_for_type_section',
            field=models.BooleanField(default=False),
        ),
    ]
