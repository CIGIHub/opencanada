# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0004_footercontent_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentBlockLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            name='ContentMenuLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.TextField()),
                ('link', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(related_name='menu_links', to='themes.MenuItem')),
                ('menu', modelcluster.fields.ParentalKey(related_name='item_links', to='themes.Menu')),
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
        migrations.RenameModel(
            old_name='FooterTextBlock',
            new_name='TextBlock',
        ),
        migrations.RemoveField(
            model_name='footerblocklink',
            name='block',
        ),
        migrations.RemoveField(
            model_name='footerblocklink',
            name='footer',
        ),
        migrations.RemoveField(
            model_name='footerfollowlink',
            name='block',
        ),
        migrations.RemoveField(
            model_name='footerfollowlink',
            name='footer',
        ),
        migrations.RemoveField(
            model_name='footerlogolink',
            name='block',
        ),
        migrations.RemoveField(
            model_name='footerlogolink',
            name='footer',
        ),
        migrations.RemoveField(
            model_name='theme',
            name='footer_content',
        ),
        migrations.DeleteModel(
            name='FooterBlockLink',
        ),
        migrations.DeleteModel(
            name='FooterContent',
        ),
        migrations.DeleteModel(
            name='FooterFollowLink',
        ),
        migrations.DeleteModel(
            name='FooterLogoLink',
        ),
        migrations.AddField(
            model_name='contentmenulink',
            name='menu',
            field=models.ForeignKey(related_name='content_links', to='themes.Menu'),
        ),
        migrations.AddField(
            model_name='contentmenulink',
            name='theme_content',
            field=modelcluster.fields.ForeignKey(related_name='menu_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='contentlogolink',
            name='theme_content',
            field=modelcluster.fields.ForeignKey(related_name='logo_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='contentfollowlink',
            name='theme_content',
            field=modelcluster.fields.ForeignKey(related_name='follow_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='contentblocklink',
            name='block',
            field=models.ForeignKey(related_name='content_links', to='themes.TextBlock'),
        ),
        migrations.AddField(
            model_name='contentblocklink',
            name='theme_content',
            field=modelcluster.fields.ForeignKey(related_name='block_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='theme',
            name='content',
            field=models.ForeignKey(to='themes.ThemeContent', null=True),
        ),
    ]
