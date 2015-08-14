# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0037_articlepage_hide_author_block'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecategory',
            name='include_main_image',
        ),
        migrations.RemoveField(
            model_name='articlepage',
            name='hide_author_block',
        ),
        migrations.AddField(
            model_name='articlepage',
            name='include_author_block',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='include_main_image',
            field=models.BooleanField(default=True),
        ),
    ]
