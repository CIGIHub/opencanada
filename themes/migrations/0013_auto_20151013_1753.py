# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0012_auto_20151013_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentBackgroundImageLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block', models.ForeignKey(related_name='content_links', to='themes.BackgroundImageBlock')),
            ],
        ),
        migrations.RemoveField(
            model_name='themecontent',
            name='backgroundImage',
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
            model_name='contentbackgroundimagelink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(related_name='backgroundImage_links', to='themes.ThemeContent'),
        ),
    ]
