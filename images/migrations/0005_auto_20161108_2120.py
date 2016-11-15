# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_auto_20160606_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributedrendition',
            name='filter_spec',
            field=models.CharField(default='', max_length=255, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='attributedrendition',
            name='filter',
            field=models.ForeignKey(related_name='+', blank=True, to='wagtailimages.Filter', null=True),
        ),
    ]
