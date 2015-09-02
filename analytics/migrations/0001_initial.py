# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analytics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_period_views', models.PositiveIntegerField(default=0)),
                ('page', models.OneToOneField(to='wagtailcore.Page')),
            ],
            options={
                'verbose_name_plural': 'analytics',
            },
        ),
    ]
