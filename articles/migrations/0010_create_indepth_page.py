# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_features_page(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    InDepthListPage = apps.get_model("articles", "InDepthListPage")
    home_page = Page.objects.get(slug="home")
    ContentType = apps.get_model("contenttypes", "ContentType")
    indepth_list_page_content_type = ContentType.objects.get_for_model(InDepthListPage)

    # Create features page
    indepth_page = InDepthListPage.objects.create(
        title="InDepth",
        slug='indepth',
        content_type=indepth_list_page_content_type,
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
        ('articles', '0009_auto_20150619_2156'),
    ]

    operations = [
        migrations.RunPython(create_features_page),
    ]
