# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0019_staticjsondata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StaticJsonData',
        ),
    ]
