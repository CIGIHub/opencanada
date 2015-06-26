# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import VERSION as DJANGO_VERSION
from django.db import migrations, models


def create_pages(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    InDepthListPage = apps.get_model("articles", "InDepthListPage")
    ArticleListPage = apps.get_model("articles", "ArticleListPage")
    home_page = Page.objects.get(slug="home")
    ContentType = apps.get_model("contenttypes", "ContentType")

    article_list_page_content_type, created = ContentType.objects.get_or_create(
        model='articlelistpage',
        app_label='articles'
    )
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

    indepth_list_page_content_type, created = ContentType.objects.get_or_create(
        model='indepthlistpage',
        app_label='articles'
    )

    # Create indepth page
    indepth_page = InDepthListPage.objects.create(
        title="InDepth",
        slug='indepth',
        content_type_id=indepth_list_page_content_type.pk,
        path='000100010002',
        depth=3,
        numchild=0,
        url_path='/home/indepth/',
    )

    home_page.numchild += 1
    home_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('core', '__latest__'),
        ('articles', '0002_articleauthorlink_author'),
    ]

    operations = [
        migrations.RunPython(create_pages),
    ]
