# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import VERSION as DJANGO_VERSION
from django.contrib.contenttypes.management import update_contenttypes
from django.db import migrations


def create_indepth_page(apps, schema_editor):
    update_contenttypes(apps.app_configs['articles'], interactive=False)
    Page = apps.get_model("wagtailcore", "Page")
    InDepthListPage = apps.get_model("articles", "InDepthListPage")
    home_page = Page.objects.get(slug="home")
    ContentType = apps.get_model("contenttypes", "ContentType")
    # indepth_list_page_content_type = ContentType.objects.get_for_model(InDepthListPage)
    indepth_list_page_content_type = ContentType.objects.get(pk=1)
    
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
        migrations.RunPython(create_indepth_page),
    ]
