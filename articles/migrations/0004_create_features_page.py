# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_features_page(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    ArticleListPage = apps.get_model("articles", "ArticleListPage")
    home_page = Page.objects.get(slug="home")
    ContentType = apps.get_model("contenttypes", "ContentType")
    article_list_page_content_type = ContentType.objects.get_for_model(ArticleListPage)

    # Create features page
    features_page = ArticleListPage.objects.create(
        title="Features",
        slug='features',
        content_type=article_list_page_content_type,
        path='000100010001',
        depth=3,
        numchild=0,
        url_path='/home/features/',
    )

    home_page.numchild += 1
    home_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('core', '__latest__'),
        ('articles', '0003_articlelistpage'),
    ]

    operations = [
        migrations.RunPython(create_features_page),
    ]
