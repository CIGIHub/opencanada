# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_auto_20150715_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureStyle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('number_of_columns', models.IntegerField(default=1)),
                ('number_of_rows', models.IntegerField(default=1)),
                ('include_image', models.BooleanField(default=False)),
                ('overlay_text', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=30, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='headline',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=30, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='seriespage',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=30, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
