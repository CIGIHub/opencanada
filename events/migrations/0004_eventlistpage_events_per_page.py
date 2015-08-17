# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_eventpage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlistpage',
            name='events_per_page',
            field=models.IntegerField(default=20),
        ),
    ]
