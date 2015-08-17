# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0041_auto_20150814_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalarticlelistpage',
            name='articles_per_page',
            field=models.IntegerField(default=20),
        ),
    ]
