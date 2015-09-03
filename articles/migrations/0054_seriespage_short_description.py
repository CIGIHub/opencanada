# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0053_auto_20150903_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriespage',
            name='short_description',
            field=wagtail.wagtailcore.fields.RichTextField(default='', blank=True),
        ),
    ]
