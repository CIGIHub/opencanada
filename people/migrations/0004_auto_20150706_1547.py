# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_create_list_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributorpage',
            name='headshot',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='images.AttributedImage', null=True),
        ),
    ]
