# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_homepage_featured_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='number_of_articles',
            field=models.IntegerField(default=12),
        ),
    ]
