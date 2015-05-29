# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_legacyarticlepage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='legacyarticlepage',
            name='id',
        ),
    ]
