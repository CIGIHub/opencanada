# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0018_auto_20151207_1852'),
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
    ]
