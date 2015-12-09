# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0020_delete_staticjsondata'),
    ]

    operations = [
        migrations.AddField(
            model_name='themecontent',
            name='json_file',
            field=models.CharField(help_text='Only provide if you know your template will be filled with the contents of a JSON data file.', max_length=255, null=True, verbose_name='JSON file', blank=True),
        ),
    ]
