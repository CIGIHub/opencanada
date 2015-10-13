# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0072_auto_20151013_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlebackgroundimagelink',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articlebackgroundimagelink',
            name='background_image',
        ),
        migrations.AlterModelOptions(
            name='backgroundimageblock',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='backgroundimageblock',
            name='article',
            field=modelcluster.fields.ParentalKey(related_name='background_image_links', null=True, to='articles.ArticlePage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='backgroundimageblock',
            name='sort_order',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.DeleteModel(
            name='ArticleBackgroundImageLink',
        ),
    ]
