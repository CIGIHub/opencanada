# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_seriespage_subtitle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seriespage',
            old_name='image',
            new_name='main_image',
        ),
    ]
