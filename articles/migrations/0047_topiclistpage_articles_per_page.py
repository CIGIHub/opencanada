# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0046_articlepage_include_main_image_overlay'),
    ]

    operations = [
        migrations.AddField(
            model_name='topiclistpage',
            name='articles_per_page',
            field=models.IntegerField(default=20),
        ),
    ]
