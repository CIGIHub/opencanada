# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-02 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_auto_20170124_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributedrendition',
            name='filter',
        ),
        migrations.AlterField(
            model_name='attributedrendition',
            name='focal_point_key',
            field=models.CharField(blank=True, default='', editable=False, max_length=16),
        ),
    ]
