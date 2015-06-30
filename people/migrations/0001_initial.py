# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import wagtail.wagtailcore.blocks
from django.db import migrations, models

import people.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributorPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('first_name', models.CharField(default='', max_length=255, blank=True)),
                ('last_name', models.CharField(default='', max_length=255, blank=True)),
                ('nickname', models.CharField(default='', max_length=1024, blank=True)),
                ('email', models.EmailField(default='', max_length=254, blank=True)),
                ('twitter_handle', models.CharField(default='', max_length=16, blank=True)),
                ('short_bio', models.TextField(default='', blank=True)),
                ('long_bio', models.TextField(default='', blank=True)),
                ('headshot', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
