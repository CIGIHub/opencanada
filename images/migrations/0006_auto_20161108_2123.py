# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from wagtail.wagtailimages.utils import get_fill_filter_spec_migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_auto_20161108_2120'),
    ]

    forward, reverse = get_fill_filter_spec_migrations('images', 'AttributedRendition')
    operations = [
        migrations.RunPython(forward, reverse),
    ]
