# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20150706_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='indepthpage',
            name='subtitle',
            field=wagtail.wagtailcore.fields.RichTextField(default='', blank=True),
        ),
    ]
