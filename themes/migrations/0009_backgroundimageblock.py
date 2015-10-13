# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20150923_1943'),
        ('themes', '0008_logoblock_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImageBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=2048, null=True, blank=True)),
                ('image', models.ForeignKey(to='images.AttributedImage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
