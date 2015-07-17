# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_homepage_number_of_articles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='number_of_articles',
            new_name='number_of_rows_of_articles',
        ),
    ]
