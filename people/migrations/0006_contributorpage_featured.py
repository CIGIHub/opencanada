# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_contributorlistpage_people_per_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributorpage',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
