# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0024_auto_20150722_1928'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecategory',
            options={'ordering': ['name'], 'verbose_name_plural': 'Article Categories'},
        ),
        migrations.AlterModelOptions(
            name='colour',
            options={'ordering': ['name']},
        ),
    ]
