# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_sitedefaults'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitedefaults',
            options={'verbose_name_plural': 'Site Defaults'},
        ),
        migrations.AlterField(
            model_name='sitedefaults',
            name='site',
            field=models.OneToOneField(related_name='default_settings', to='wagtailcore.Site'),
        ),
    ]
