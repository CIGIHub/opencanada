# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0080_auto_20151126_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='title_size',
            field=models.CharField(default='medium', max_length=20, choices=[('small', 'Smaller'), ('medium', 'Medium (default 50px)'), ('large', 'Larger')]),
        ),
        migrations.AddField(
            model_name='externalarticlepage',
            name='title_size',
            field=models.CharField(default='medium', max_length=20, choices=[('small', 'Smaller'), ('medium', 'Medium (default 50px)'), ('large', 'Larger')]),
        ),
        migrations.AddField(
            model_name='headline',
            name='title_size',
            field=models.CharField(default='medium', max_length=20, choices=[('small', 'Smaller'), ('medium', 'Medium (default 50px)'), ('large', 'Larger')]),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='title_size',
            field=models.CharField(default='medium', max_length=20, choices=[('small', 'Smaller'), ('medium', 'Medium (default 50px)'), ('large', 'Larger')]),
        ),
    ]
