# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0013_auto_20151013_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backgroundimageblock',
            name='image',
        ),
        migrations.RemoveField(
            model_name='contentbackgroundimagelink',
            name='block',
        ),
        migrations.RemoveField(
            model_name='contentbackgroundimagelink',
            name='theme_content',
        ),
        migrations.DeleteModel(
            name='BackgroundImageBlock',
        ),
        migrations.DeleteModel(
            name='ContentBackgroundImageLink',
        ),
    ]
