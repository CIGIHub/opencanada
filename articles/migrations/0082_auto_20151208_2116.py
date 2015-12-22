# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0081_auto_20151126_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticJsonData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('json', models.TextField()),
                ('template', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='articlepage',
            name='static_json',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.StaticJsonData', null=True),
        ),
    ]
