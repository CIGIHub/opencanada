# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0071_auto_20151013_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundimageblock',
            name='position',
            field=models.CharField(default='left top', max_length=20, choices=[('left top', 'left top'), ('left center', 'left center'), ('left bottom', 'left bottom'), ('right top', 'right top'), ('right center', 'right center'), ('right bottom', 'right bottom'), ('center top', 'center top'), ('center center', 'center center'), ('center bottom', 'center bottom')]),
        ),
    ]
