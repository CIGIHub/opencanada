# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_fontstyle_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='number_of_articles',
            field=models.IntegerField(default=12),
        ),
    ]
