# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_auto_20161108_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributedrendition',
            name='filter_spec',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='attributedrendition',
            unique_together=set([('image', 'filter_spec', 'focal_point_key')]),
        ),
    ]
