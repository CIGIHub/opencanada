# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordpress_importer', '0002_postimport_article_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportDownloadError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=1024)),
                ('status_code', models.IntegerField(null=True)),
            ],
        ),
    ]
