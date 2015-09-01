# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0049_articlelistpage_filter_for_interviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=45, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='externalarticlepage',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=45, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='headline',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=45, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='seriespage',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=45, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
