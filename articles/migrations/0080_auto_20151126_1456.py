# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0079_auto_20151126_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fontstyle',
            name='text_colour',
        ),
        migrations.RemoveField(
            model_name='articlepage',
            name='font_style',
        ),
        migrations.RemoveField(
            model_name='externalarticlepage',
            name='font_style',
        ),
        migrations.RemoveField(
            model_name='headline',
            name='font_style',
        ),
        migrations.RemoveField(
            model_name='seriespage',
            name='font_style',
        ),
        migrations.DeleteModel(
            name='Colour',
        ),
        migrations.DeleteModel(
            name='FontStyle',
        ),
    ]
