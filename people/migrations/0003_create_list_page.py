# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import VERSION as DJANGO_VERSION
from django.db import migrations, models


def create_page(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    ContributorListPage = apps.get_model("people", "ContributorListPage")
    home_page = Page.objects.get(slug="home")
    ContentType = apps.get_model("contenttypes", "ContentType")

    contributor_list_page_content_type, created = ContentType.objects.get_or_create(
        model='contributorlistpage',
        app_label='people',
        defaults={'name': 'contributorlistpage'} if DJANGO_VERSION < (1, 8) else {}
    )
    # Create features page
    features_page = ContributorListPage.objects.create(
        title="Contributors",
        slug='contributors',
        content_type=contributor_list_page_content_type,
        path='000100010003',
        depth=3,
        numchild=0,
        url_path='/home/contributors/',
    )
    home_page.numchild += 1
    home_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_contributorlistpage'),
    ]

    operations = [
        migrations.RunPython(create_page),
    ]
