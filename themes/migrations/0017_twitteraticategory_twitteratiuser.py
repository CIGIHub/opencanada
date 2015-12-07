# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0016_auto_20151014_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitteratiCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TwitteratiUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('twitter_handle', models.CharField(max_length=16)),
                ('biography', models.CharField(max_length=255)),
                ('category', models.ForeignKey(to='themes.TwitteratiCategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
