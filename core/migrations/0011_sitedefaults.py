# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('core', '0010_auto_20150818_1942'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteDefaults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_external_article_source_logo', models.ForeignKey(related_name='+', to='images.AttributedImage', on_delete=models.deletion.CASCADE)),
                ('site', models.OneToOneField(related_name='+', to='wagtailcore.Site', on_delete=models.deletion.CASCADE)),
            ],
        ),
    ]
