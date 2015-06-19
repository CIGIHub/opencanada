# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_indepthlistpage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indeptharticlelink',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='indeptharticlelink',
            name='sort_order',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
    ]
