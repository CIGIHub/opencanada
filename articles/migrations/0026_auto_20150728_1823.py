# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('images', '0001_initial'),
        ('articles', '0025_auto_20150724_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('sticky', models.BooleanField(default=False)),
                ('image_overlay_opacity', models.PositiveIntegerField(default=30, help_text='Set the value from 0 (Solid overlay, original image not visible) to 100 (No overlay, original image completely visible)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('body', wagtail.core.fields.RichTextField()),
                ('website_link', models.URLField(max_length=255)),
                ('feature_style', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.FeatureStyle', null=True)),
                ('font_style', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.FontStyle', null=True)),
                ('image_overlay_color', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=1, to='articles.Colour', null=True)),
                ('main_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='images.AttributedImage', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(max_length=255)),
                ('logo', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='images.AttributedImage', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='externalarticlepage',
            name='source',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.Source', null=True),
        ),
    ]
