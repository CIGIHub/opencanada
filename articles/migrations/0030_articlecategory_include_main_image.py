# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0029_auto_20150811_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecategory',
            name='include_main_image',
            field=models.BooleanField(default=True),
        ),
    ]
