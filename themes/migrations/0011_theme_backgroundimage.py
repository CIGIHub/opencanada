# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0010_auto_20151013_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='backgroundImage',
            field=models.ForeignKey(to='themes.BackgroundImageBlock', null=True),
        ),
    ]
