# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import articles.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_create_colours'),
    ]

    operations = [
        migrations.CreateModel(
            name='FontStyle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('font_size', models.FloatField(default=1, help_text='The size of the fonts in ems.')),
                ('line_size', models.FloatField(default=100, help_text='The line height as a percentage.')),
                ('text_colour', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.Colour', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='articlepage',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=50, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='headline',
            name='image_overlay_opacity',
            field=models.PositiveIntegerField(default=50, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='font_style',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.FontStyle', null=True),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='image_overlay_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.Colour', null=True),
        ),
        migrations.AddField(
            model_name='headline',
            name='font_style',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.FontStyle', null=True),
        ),
        migrations.AddField(
            model_name='headline',
            name='image_overlay_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.Colour', null=True),
        ),
    ]
