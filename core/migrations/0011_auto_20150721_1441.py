# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_searchsuggestion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchsuggestion',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='searchsuggestion',
            name='sort_order',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
    ]
