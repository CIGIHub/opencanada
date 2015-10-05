# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0002_add_verbose_names'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('analytics', '0001_initial'),
        ('content_notes', '0003_auto_20150930_2002'),
        ('basic_site', '0005_basicstreampage'),
        ('newsletter', '0015_newsletterexternalarticlelink2'),
        ('wagtailforms', '0002_add_verbose_names'),
        ('articles', '0066_assign_theme_to_pages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapteredarticlepage',
            name='articlepage_ptr',
        ),
        migrations.DeleteModel(
            name='ChapteredArticlePage',
        ),
    ]
