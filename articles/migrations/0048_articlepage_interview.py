# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0047_topiclistpage_articles_per_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='interview',
            field=models.BooleanField(default=False),
        ),
    ]
