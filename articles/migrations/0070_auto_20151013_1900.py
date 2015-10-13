# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0069_articlebackgroundimagelink'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlebackgroundimagelink',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='articlebackgroundimagelink',
            name='sort_order',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
    ]
