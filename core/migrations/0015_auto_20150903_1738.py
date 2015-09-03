# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_homepage_full_bleed_image_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='full_bleed_image_size',
            field=models.PositiveSmallIntegerField(default=90, help_text='Enter a value from 0 - 100, indicating the percentage of the screen to use for the featured image layout.'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='number_of_columns_of_articles',
            field=models.IntegerField(default=3, verbose_name='Columns'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='number_of_columns_of_external_articles',
            field=models.IntegerField(default=2, verbose_name='Columns'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='number_of_columns_of_series',
            field=models.IntegerField(default=4, verbose_name='Columns'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='number_of_columns_of_visualizations',
            field=models.IntegerField(default=2, verbose_name='Columns'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='number_of_rows_of_articles',
            field=models.IntegerField(default=12, verbose_name='Rows'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='number_of_rows_of_external_articles',
            field=models.IntegerField(default=2, verbose_name='Rows'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='number_of_rows_of_series',
            field=models.IntegerField(default=1, verbose_name='Rows'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='number_of_rows_of_visualizations',
            field=models.IntegerField(default=2, verbose_name='Rows'),
        ),
    ]
