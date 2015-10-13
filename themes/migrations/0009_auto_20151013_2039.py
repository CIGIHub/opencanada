# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0008_logoblock_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentblocklink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='block_links', to='themes.ThemeContent'),
        ),
        migrations.AlterField(
            model_name='contentfollowlink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='follow_links', to='themes.ThemeContent'),
        ),
        migrations.AlterField(
            model_name='contentlogolink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='logo_links', to='themes.ThemeContent'),
        ),
    ]
