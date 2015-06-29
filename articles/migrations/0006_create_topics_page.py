# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_pages(apps, schema_editor):
    Page = apps.get_model("wagtailcore", "Page")
    TopicListPage = apps.get_model("articles", "TopicListPage")
    home_page = Page.objects.get(slug="home")
    ContentType = apps.get_model("contenttypes", "ContentType")

    topic_list_page_content_type, created = ContentType.objects.get_or_create(
        model='topiclistpage',
        app_label='articles'
    )
    # Create topics page
    topics_page = TopicListPage.objects.create(
        title="Topics",
        slug='topics',
        content_type_id=topic_list_page_content_type.pk,
        path='000100010004',
        depth=3,
        numchild=0,
        url_path='/home/topics/',
    )
    home_page.numchild += 1
    home_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('articles', '0005_auto_20150626_1948'),
    ]

    operations = [
        migrations.RunPython(create_pages),
    ]
