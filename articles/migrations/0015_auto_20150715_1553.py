# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import articles.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20150713_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('rgb_value', models.CharField(max_length=7)),
            ],
        ),
    ]
