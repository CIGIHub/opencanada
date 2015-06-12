# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_features_page(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    HomePage = apps.get_model("core", "HomePage")

    wagtail_home_page = Page.objects.get(slug="home")
    wagtail_home_page.delete()

    ContentType = apps.get_model("contenttypes", "ContentType")
    home_page_content_type = ContentType.objects.get_for_model(HomePage)

    # Create home page
    home_page = HomePage.objects.create(
        title="Home",
        slug='home',
        content_type=home_page_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_features_page),
    ]
