# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import django.db.models.deletion
import themes.models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0025_remove_theme_json_file'),
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(default='', max_length=255, blank=True)),
                ('description', wagtail.wagtailcore.fields.RichTextField(default='', blank=True)),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=themes.models.get_default_theme, to='themes.Theme', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
