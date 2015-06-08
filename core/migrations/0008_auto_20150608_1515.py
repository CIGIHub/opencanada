# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('basic_site', '0004_basicblock_image'),
        ('wagtailforms', '0002_add_verbose_names'),
        ('wagtailsearch', '0002_add_verbose_names'),
        ('wagtailredirects', '0002_add_verbose_names'),
        ('core', '0007_articlepage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='articlepage',
            name='page_ptr',
        ),
        migrations.AlterField(
            model_name='legacyarticlepage',
            name='excerpt',
            field=wagtail.wagtailcore.fields.RichTextField(),
        ),
        migrations.DeleteModel(
            name='ArticlePage',
        ),
    ]
