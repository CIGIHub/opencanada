# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20150707_2303'),
        ('wordpress_importer', '0002_postimport_article_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_slug', models.CharField(max_length=1024)),
                ('topic', models.ForeignKey(to='articles.Topic', null=True)),
            ],
        ),
    ]
