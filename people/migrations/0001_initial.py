# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('nickname', models.CharField(default=b'', max_length=1024, blank=True)),
                ('email', models.EmailField(default=b'', max_length=254, blank=True)),
                ('twitter_handle', models.CharField(default=b'', max_length=16, blank=True)),
                ('short_bio', models.TextField(default=b'', blank=True)),
                ('long_bio', models.TextField(default=b'', blank=True)),
            ],
        ),
    ]
