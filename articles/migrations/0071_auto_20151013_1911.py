# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20150923_1943'),
        ('articles', '0070_auto_20151013_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImageBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('position', models.TextField(blank=True, null=True, choices=[('left top', 'left top'), ('left center', 'left center'), ('left bottom', 'left bottom'), ('right top', 'right top'), ('right center', 'right center'), ('right bottom', 'right bottom'), ('center top', 'center top'), ('center center', 'center center'), ('center bottom', 'center bottom')])),
                ('image', models.ForeignKey(to='images.AttributedImage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='articlebackgroundimagelink',
            name='background_image',
            field=models.ForeignKey(related_name='+', to='articles.BackgroundImageBlock'),
        ),
    ]
