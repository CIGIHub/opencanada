# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20150923_1943'),
        ('themes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=1024)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FooterBlockLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='FooterContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_email', models.EmailField(help_text='Only provide if this should be different from the site default email contact address.', max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FooterFollowLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block', models.ForeignKey(related_name='footer_links', to='themes.FollowLink')),
                ('footer', modelcluster.fields.ParentalKey(related_name='follow_links', to='themes.FooterContent')),
            ],
        ),
        migrations.CreateModel(
            name='FooterLogoLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='FooterTextBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('heading', models.TextField(default='', blank=True)),
                ('content', wagtail.wagtailcore.fields.RichTextField(default='', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogoBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ForeignKey(to='images.AttributedImage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='footerlogolink',
            name='block',
            field=models.ForeignKey(related_name='footer_links', to='themes.LogoBlock'),
        ),
        migrations.AddField(
            model_name='footerlogolink',
            name='footer',
            field=modelcluster.fields.ParentalKey(related_name='logo_links', to='themes.FooterContent'),
        ),
        migrations.AddField(
            model_name='footerblocklink',
            name='block',
            field=models.ForeignKey(related_name='footer_links', to='themes.FooterTextBlock'),
        ),
        migrations.AddField(
            model_name='footerblocklink',
            name='footer',
            field=modelcluster.fields.ParentalKey(related_name='block_links', to='themes.FooterContent'),
        ),
    ]
