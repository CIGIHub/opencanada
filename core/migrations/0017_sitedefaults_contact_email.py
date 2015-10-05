# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_homepage_number_of_columns_of_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitedefaults',
            name='contact_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
