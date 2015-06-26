# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.contrib.wagtailroutablepage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('articles', '0004_headline'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicListPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.SlugField(unique=True, max_length=255, blank=True),
        ),
    ]
