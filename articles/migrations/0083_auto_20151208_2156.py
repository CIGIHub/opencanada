# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0082_auto_20151208_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticJsonDataContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('json', models.TextField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.DeleteModel(
            name='StaticJsonData',
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='static_json',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.StaticJsonDataContent', null=True),
        ),
    ]
