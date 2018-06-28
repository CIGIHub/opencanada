# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.images.models
from django.conf import settings
import django.db.models.deletion
import wagtail.core.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('images', '0002_auto_20150923_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributedimage',
            name='collection',
            field=models.ForeignKey(related_name='+', default=wagtail.core.models.get_root_collection_id, verbose_name='collection', to='wagtailcore.Collection'),
        ),
        migrations.AlterField(
            model_name='attributedimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at', db_index=True),
        ),
        migrations.AlterField(
            model_name='attributedimage',
            name='file',
            field=models.ImageField(height_field='height', upload_to=wagtail.images.models.get_upload_to, width_field='width', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='attributedimage',
            name='height',
            field=models.IntegerField(verbose_name='height', editable=False),
        ),
        migrations.AlterField(
            model_name='attributedimage',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=None, verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='attributedimage',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='attributedimage',
            name='uploaded_by_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='uploaded by user'),
        ),
        migrations.AlterField(
            model_name='attributedimage',
            name='width',
            field=models.IntegerField(verbose_name='width', editable=False),
        ),
    ]
