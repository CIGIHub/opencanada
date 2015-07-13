# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20150707_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='style',
            field=models.CharField(default='simple', max_length=20, choices=[('simple', 'Single Column - Text Only'), ('simpleimage', 'Single Column - Text and Image'), ('coverimage', 'Full Width - Text overlayed on image'), ('tallcoverimage', 'Full Width - Double Height - Text overlayed on image')]),
        ),
    ]
