# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0002_auto_20151002_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='footer_content',
            field=models.ForeignKey(to='themes.FooterContent', null=True),
        ),
    ]
