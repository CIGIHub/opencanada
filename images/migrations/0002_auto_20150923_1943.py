# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributedimage',
            name='file_size',
            field=models.PositiveIntegerField(null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='attributedimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at', db_index=True),
        ),
    ]
