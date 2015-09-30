# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0061_auto_20150928_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endnote',
            name='article',
        ),
        migrations.DeleteModel(
            name='EndNote',
        ),
    ]
