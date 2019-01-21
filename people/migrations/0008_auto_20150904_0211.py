# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_auto_20150825_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributorpage',
            name='short_bio',
            field=wagtail.core.fields.RichTextField(default='', blank=True),
        ),
    ]
