# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0022_auto_20151209_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='themecontent',
            name='json_file',
        ),
        migrations.AddField(
            model_name='theme',
            name='json_file',
            field=models.CharField(help_text='Only provide if you know your template will be filled with the contents of a JSON data file.', max_length=255, null=True, verbose_name='JSON file', blank=True),
        ),
    ]
