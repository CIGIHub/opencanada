# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150728_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='body',
            field=wagtail.core.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]
