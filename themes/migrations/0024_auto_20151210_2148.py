# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0023_auto_20151209_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='json_file',
            field=models.FileField(upload_to=b'', max_length=255, blank=True, help_text='Only provide if you know your template will be filled with the contents of a JSON data file.', null=True, verbose_name='JSON file'),
        ),
    ]
