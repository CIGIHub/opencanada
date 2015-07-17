# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150716_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='number_of_columns_of_articles',
            field=models.IntegerField(default=3),
        ),
    ]
