# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_auto_20150715_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriespage',
            name='font_style',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.FontStyle', null=True),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='image_overlay_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.Colour', null=True),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=50, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
