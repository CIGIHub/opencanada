# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150624_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='fontstyle',
            name='name',
            field=models.CharField(default='Black', max_length=1024),
            preserve_default=False,
        ),
    ]
