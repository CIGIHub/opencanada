# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0015_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followlink',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='logoblock',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='textblock',
            name='slug',
        ),
        migrations.AddField(
            model_name='followlink',
            name='usage',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='logoblock',
            name='usage',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='textblock',
            name='usage',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
    ]
