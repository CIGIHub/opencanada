# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20150706_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriespage',
            name='subtitle',
            field=wagtail.wagtailcore.fields.RichTextField(default='', blank=True),
        ),
    ]
