# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_homepage_number_of_columns_of_articles'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchSuggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phrase', models.CharField(max_length=1024)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
