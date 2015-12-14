# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import articles.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0084_auto_20151209_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='json_file',
            field=articles.fields.WagtailFileField(upload_to=b'', max_length=255, blank=True, help_text='Only provide if you know your template will be filled with the contents of a JSON data file.', null=True, verbose_name='JSON file'),
        ),
    ]
