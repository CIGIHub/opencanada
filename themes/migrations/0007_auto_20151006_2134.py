# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0006_create_themes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentmenulink',
            name='menu',
        ),
        migrations.RemoveField(
            model_name='contentmenulink',
            name='theme_content',
        ),
        migrations.RemoveField(
            model_name='menuitemlink',
            name='item',
        ),
        migrations.RemoveField(
            model_name='menuitemlink',
            name='menu',
        ),
        migrations.DeleteModel(
            name='ContentMenuLink',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='MenuItem',
        ),
        migrations.DeleteModel(
            name='MenuItemLink',
        ),
    ]
