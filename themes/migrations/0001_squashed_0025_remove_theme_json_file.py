# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
import wagtail.core.fields
from django.db import migrations, models


def create_themes(apps, schema_editor):
    Theme = apps.get_model("themes", "Theme")
    ThemeContent = apps.get_model("themes", "ThemeContent")
    FollowLink = apps.get_model("themes", "FollowLink")
    ContentFollowLink = apps.get_model("themes", "ContentFollowLink")
    TextBlock = apps.get_model("themes", "TextBlock")
    ContentBlockLink = apps.get_model("themes", "ContentBlockLink")
    HomePage = apps.get_model('core', 'HomePage')

    about_block = TextBlock.objects.create(
        name='About Block',
        heading='About',
        content='Open Canada is a Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. quis nostrud exercitation.'
    )

    masthead_block = TextBlock.objects.create(
        name='Masthead Block',
        heading='Masthead',
        content="""<p><a href="https://twitter.com/taylor_owen">@Taylor Owen</a> / Editor-in-Chief</p>
                <p><a href="https://twitter.com/eva_sita">@Eva Salinas</a> / Managing Editor</p>
                <p><a href="https://twitter.com/cattsalikis">@Catherine Tsalikis</a> / Journalist &amp; Editor</p>"""
    )

    newsletter_block = TextBlock.objects.create(
        name='Newsletter Block',
        heading='Weekly Newsletter',
        content=""
    )

    follow_block = TextBlock.objects.create(
        name='Follow Block',
        heading='Follow',
        content=""
    )

    tagline_block = TextBlock.objects.create(
        name='Tagline Block',
        heading='',
        content="OpenCanada.org is a publication of the Canadian International Council, the Centre for International Governance Innovation and the Bill Graham Centre"
    )

    twitter = FollowLink.objects.create(
        name="Twitter",
        link="https://twitter.com/opencanada"
    )

    facebook = FollowLink.objects.create(
        name="Facebook",
        link="https://facebook.com/opencanada"
    )

    google_plus = FollowLink.objects.create(
        name="Google Plus",
        link="#"
    )

    rss_feed = FollowLink.objects.create(
        name="RSS Feed",
        link="/feed/"
    )

    default_content = ThemeContent.objects.create(
        name="OpenCanada Standard",
    )

    ContentBlockLink.objects.create(
        theme_content_id=default_content.id,
        block_id=about_block.id
    )

    ContentBlockLink.objects.create(
        theme_content_id=default_content.id,
        block_id=masthead_block.id
    )

    ContentBlockLink.objects.create(
        theme_content_id=default_content.id,
        block_id=newsletter_block.id
    )

    ContentBlockLink.objects.create(
        theme_content_id=default_content.id,
        block_id=follow_block.id
    )

    ContentBlockLink.objects.create(
        theme_content_id=default_content.id,
        block_id=tagline_block.id
    )

    ContentFollowLink.objects.create(
        theme_content_id=default_content.id,
        block_id=twitter.id
    )

    ContentFollowLink.objects.create(
        theme_content_id=default_content.id,
        block_id=facebook.id
    )

    ContentFollowLink.objects.create(
        theme_content_id=default_content.id,
        block_id=google_plus.id
    )

    ContentFollowLink.objects.create(
        theme_content_id=default_content.id,
        block_id=rss_feed.id
    )

    default_theme, created = Theme.objects.get_or_create(
        name="default"
    )
    default_theme.is_default=True
    default_theme.content_id=default_content.id
    default_theme.save()

    dark, created = Theme.objects.get_or_create(
        name="dark",
        folder="themes/dark"
    )
    dark.content_id = default_content.id
    dark.save()

    light, created = Theme.objects.get_or_create(
        name="light",
        folder="themes/light"
    )
    light.content_id = default_content.id
    light.save()

    lind, created = Theme.objects.get_or_create(
        name="lind",
        folder="themes/lind"
    )
    lind.content_id = default_content.id
    lind.save()


class Migration(migrations.Migration):

    replaces = [('themes', '0001_initial'), ('themes', '0002_auto_20151002_2217'), ('themes', '0003_theme_footer_content'), ('themes', '0004_footercontent_name'), ('themes', '0005_auto_20151002_2357'), ('themes', '0006_create_themes'), ('themes', '0007_auto_20151006_2134'), ('themes', '0008_logoblock_link'), ('themes', '0009_backgroundimageblock'), ('themes', '0010_auto_20151013_1710'), ('themes', '0011_theme_backgroundimage'), ('themes', '0012_auto_20151013_1731'), ('themes', '0013_auto_20151013_1753'), ('themes', '0014_auto_20151013_1855'), ('themes', '0009_auto_20151013_2039'), ('themes', '0015_merge'), ('themes', '0016_auto_20151014_2016'), ('themes', '0017_twitteraticategory_twitteratiuser'), ('themes', '0018_auto_20151207_1852'), ('themes', '0019_staticjsondata'), ('themes', '0020_delete_staticjsondata'), ('themes', '0021_themecontent_json_file'), ('themes', '0022_auto_20151209_1434'), ('themes', '0023_auto_20151209_2025'), ('themes', '0024_auto_20151210_2148'), ('themes', '0025_remove_theme_json_file')]

    dependencies = [
        ('images', '0002_auto_20150923_1943'),
        ('core', '0017_sitedefaults_contact_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('folder', models.CharField(default=b'themes/default', max_length=1024)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FollowLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=1024)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('heading', models.TextField(default='', blank=True)),
                ('content', wagtail.core.fields.RichTextField(default='', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogoBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ForeignKey(to='images.AttributedImage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentBlockLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block', models.ForeignKey(related_name='content_links', to='themes.TextBlock')),
            ],
        ),
        migrations.CreateModel(
            name='ContentFollowLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block', models.ForeignKey(related_name='content_links', to='themes.FollowLink')),
            ],
        ),
        migrations.CreateModel(
            name='ContentLogoLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block', models.ForeignKey(related_name='content_links', to='themes.LogoBlock')),
            ],
        ),
        migrations.CreateModel(
            name='ThemeContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(help_text='Only provide if this should be different from the site default email contact address.', max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='contentlogolink',
            name='theme_content',
            field=models.ForeignKey(related_name='logo_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='contentfollowlink',
            name='theme_content',
            field=models.ForeignKey(related_name='follow_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='contentblocklink',
            name='theme_content',
            field=models.ForeignKey(related_name='block_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='theme',
            name='content',
            field=models.ForeignKey(to='themes.ThemeContent', null=True),
        ),
        migrations.AddField(
            model_name='logoblock',
            name='link',
            field=models.CharField(max_length=2048, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contentblocklink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='block_links', to='themes.ThemeContent'),
        ),
        migrations.AlterField(
            model_name='contentfollowlink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='follow_links', to='themes.ThemeContent'),
        ),
        migrations.AlterField(
            model_name='contentlogolink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='logo_links', to='themes.ThemeContent'),
        ),
        migrations.AlterField(
            model_name='contentblocklink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='block_links', to='themes.ThemeContent'),
        ),
        migrations.AlterField(
            model_name='contentfollowlink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='follow_links', to='themes.ThemeContent'),
        ),
        migrations.AlterField(
            model_name='contentlogolink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='logo_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='followlink',
            name='usage',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='logoblock',
            name='usage',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='textblock',
            name='usage',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
        migrations.RunPython(create_themes),
    ]
