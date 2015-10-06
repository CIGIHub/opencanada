# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        slug='about-block',
        heading='About',
        content='Open Canada is a Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. quis nostrud exercitation.'
    )

    masthead_block = TextBlock.objects.create(
        name='Masthead Block',
        slug='masthead-block',
        heading='Masthead',
        content="""<p><a href="https://twitter.com/taylor_owen">@Taylor Owen</a> / Editor-in-Chief</p>
                <p><a href="https://twitter.com/eva_sita">@Eva Salinas</a> / Managing Editor</p>
                <p><a href="https://twitter.com/cattsalikis">@Catherine Tsalikis</a> / Journalist &amp; Editor</p>"""
    )

    newsletter_block = TextBlock.objects.create(
        name='Newsletter Block',
        slug='newsletter-block',
        heading='Weekly Newsletter',
        content=""
    )

    follow_block = TextBlock.objects.create(
        name='Follow Block',
        slug='follow-block',
        heading='Follow',
        content=""
    )

    tagline_block = TextBlock.objects.create(
        name='Tagline Block',
        slug='tagline-block',
        heading='',
        content="OpenCanada.org is a publication of the Canadian International Council, the Centre for International Governance Innovation and the Bill Graham Centre"
    )

    twitter = FollowLink.objects.create(
        name="Twitter",
        slug="twitter",
        link="https://twitter.com/opencanada"
    )

    facebook = FollowLink.objects.create(
        name="Facebook",
        slug="facebook",
        link="https://facebook.com/opencanada"
    )

    google_plus = FollowLink.objects.create(
        name="Google Plus",
        slug="google-plus",
        link="#"
    )

    rss_feed = FollowLink.objects.create(
        name="RSS Feed",
        slug="rss-feed",
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

    dependencies = [
        ('core', '0017_sitedefaults_contact_email'),
        ('themes', '0005_auto_20151002_2357'),
    ]

    operations = [
        migrations.RunPython(create_themes),
    ]
