# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import greyjay.themes.models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0001_initial'),
        ('core', '0017_sitedefaults_contact_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='themes.Theme', null=True),
        ),
        migrations.AlterField(
            model_name='sitedefaults',
            name='contact_email',
            field=models.EmailField(default='', max_length=254, blank=True),
        ),
    ]
