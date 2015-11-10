# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0076_articlepage_video_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='video_document',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='documents.AttributedDocument', null=True),
        ),
    ]
