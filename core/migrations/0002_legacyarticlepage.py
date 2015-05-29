# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegacyArticlePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', wagtail.wagtailcore.fields.RichTextField()),
                ('excerpt', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
