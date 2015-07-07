# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_indepthpage_subtitle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indepthpage',
            old_name='image',
            new_name='main_image',
        ),
    ]
