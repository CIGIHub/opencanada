# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0007_auto_20151006_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='logoblock',
            name='link',
            field=models.CharField(max_length=2048, null=True, blank=True),
        ),
    ]
