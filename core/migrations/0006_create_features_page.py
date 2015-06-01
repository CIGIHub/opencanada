# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_features_page(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    # HomePage = apps.get_model("core", "HomePage")
    # ArticleListPage = apps.get_model("core", "ArticleListPage")

    home_page = Page.objects.get(slug="home")

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
    #
    # features_page = Page(owner=None)
    # import pdb; pdb.set_trace()
    # home_page.add_child(instance=features_page)
    home_page.numchild += 1
    home_page.save()
    #
    # features_page.title = "Features"
    # features_page.slug = "features"
    #
    # revision = features_page.save_revision(
    #     user=None,
    #     submitted_for_moderation=False,
    # )
    # revision.publish()



class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_legacyarticlepage_author'),
        ('wagtailcore', '0015_add_more_verbose_names'),
    ]

    operations = [
        migrations.RunPython(create_features_page),
    ]
