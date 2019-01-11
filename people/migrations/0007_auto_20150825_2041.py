# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_contributorpage_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributorlistpage',
            name='people_per_page',
        ),
        migrations.AlterField(
            model_name='contributorpage',
            name='long_bio',
            field=wagtail.core.fields.RichTextField(default='', blank=True),
        ),
    ]
