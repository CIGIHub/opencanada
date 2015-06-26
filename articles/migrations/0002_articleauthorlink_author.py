# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleauthorlink',
            name='author',
            field=models.ForeignKey(related_name='article_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='people.ContributorPage', null=True),
        ),
    ]
