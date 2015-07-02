# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_categories(apps, schema_editor):
    ArticleCategory = apps.get_model("articles", "ArticleCategory")

    # Create default categories
    ArticleCategory.objects.create(
        name="Feature",
        slug='feature',
    )
    ArticleCategory.objects.create(
        name="Roundtable Blog Post",
        slug='roundtable-blog-post',
    )
    ArticleCategory.objects.create(
        name="Dispatch Blog Post",
        slug='dispatch-blog-post',
    )
    ArticleCategory.objects.create(
        name="Commentary",
        slug='commentary',
    )
    ArticleCategory.objects.create(
        name="Essay",
        slug='essay',
    )
    ArticleCategory.objects.create(
        name="Infographic",
        slug='infographic',
    )
    ArticleCategory.objects.create(
        name="Interview",
        slug='interview',
    )
    ArticleCategory.objects.create(
        name="Explainer",
        slug='explainer',
    )
    ArticleCategory.objects.create(
        name="Rapid Response",
        slug='rapid-response',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20150702_1954'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
