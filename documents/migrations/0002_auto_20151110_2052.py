# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributeddocument',
            name='credit',
            field=models.CharField(default='', max_length=1024, verbose_name='Credit', blank=True),
        ),
        migrations.AlterField(
            model_name='attributeddocument',
            name='source',
            field=models.CharField(default='', max_length=1024, verbose_name='Source', blank=True),
        ),
        migrations.AlterField(
            model_name='attributeddocument',
            name='usage_restrictions',
            field=models.TextField(default='', verbose_name='Usage Restrictions', blank=True),
        ),
    ]
