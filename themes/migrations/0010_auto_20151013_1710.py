# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0009_backgroundimageblock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundimageblock',
            name='position',
            field=models.CharField(help_text='For example: top center', max_length=2048, null=True, blank=True),
        ),
    ]
