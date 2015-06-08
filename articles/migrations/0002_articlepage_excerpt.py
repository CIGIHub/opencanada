# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='excerpt',
            field=wagtail.wagtailcore.fields.RichTextField(default='', blank=True),
        ),
    ]
