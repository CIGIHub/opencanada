# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_features_page(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    ContentType = apps.get_model("contenttypes", "ContentType")
    page_content_type = ContentType.objects.get_for_model(Page)

    # Create features page
    features_page = Page.objects.create(
        title="Features",
        slug='features',
        content_type=page_content_type,
        path='000100010001',
        depth=3,
        numchild=0,
        url_path='/home/features/',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_legacyarticlepage_author'),
    ]

    operations = [
        migrations.RunPython(create_features_page),
    ]
