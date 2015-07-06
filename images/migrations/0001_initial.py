# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import taggit.managers
import wagtail.wagtailadmin.taggable
import wagtail.wagtailimages.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('wagtailimages', '0006_add_verbose_names'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributedImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_upload_to, width_field='width', verbose_name='File')),
                ('width', models.IntegerField(verbose_name='Width', editable=False)),
                ('height', models.IntegerField(verbose_name='Height', editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('focal_point_x', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_y', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_width', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_height', models.PositiveIntegerField(null=True, blank=True)),
                ('credit', models.CharField(default='', max_length=1024, blank=True)),
                ('source', models.CharField(default='', max_length=1024, blank=True)),
                ('usage_restrictions', models.TextField(default='', blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=None, verbose_name='Tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='AttributedRendition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(height_field='height', width_field='width', upload_to='images')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(default='', max_length=255, editable=False, blank=True)),
                ('filter', models.ForeignKey(related_name='+', to='wagtailimages.Filter')),
                ('image', models.ForeignKey(related_name='renditions', to='images.AttributedImage')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='attributedrendition',
            unique_together=set([('image', 'filter', 'focal_point_key')]),
        ),
    ]
