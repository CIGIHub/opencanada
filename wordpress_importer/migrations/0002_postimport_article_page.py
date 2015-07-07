# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('wordpress_importer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimport',
            name='article_page',
            field=models.ForeignKey(to='wagtailcore.Page', null=True),
        ),
    ]
