# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_projectlistpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectpage',
            name='name',
        ),
    ]
