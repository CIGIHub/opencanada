# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_themes(apps, schema_editor):
    Theme = apps.get_model("themes", "Theme")

    default_theme = Theme.objects.get(is_default=True)

    page_types = ['ArticlePage', 'SeriesPage']

    for page_type in page_types:
        page_model = apps.get_model('articles', page_type)
        pages = page_model.objects.all()

        for page in pages:
            if not page.theme:
                page.theme_id = default_theme.id
                page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0067_auto_20151005_2045'),
        ('themes', '0006_create_themes'),
    ]

    operations = [
        migrations.RunPython(set_themes),
    ]
