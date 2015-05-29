# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20150525_1813'),
        ('core', '0004_legacyarticlepage_page_ptr'),
    ]

    operations = [
        migrations.AddField(
            model_name='legacyarticlepage',
            name='author',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='people.Contributor', null=True),
        ),
    ]
