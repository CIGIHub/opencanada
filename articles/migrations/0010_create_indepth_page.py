# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import VERSION as DJANGO_VERSION
from django.db import migrations


def create_indepth_page(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    InDepthListPage = apps.get_model("articles", "InDepthListPage")
    home_page = Page.objects.get(slug="home")
    ContentType = apps.get_model("contenttypes", "ContentType")

    indepth_list_page_content_type, created = ContentType.objects.get_or_create(
        model='indepthlistpage',
        app_label='articles',
        defaults={'name': 'indepthlistpage'} if DJANGO_VERSION < (1, 8) else {}
    )

    print(indepth_list_page_content_type.pk)

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
        ('articles', '0009_auto_20150619_2156'),
        ('core', '__latest__'),
    ]

    operations = [
        migrations.RunPython(create_indepth_page),
    ]
