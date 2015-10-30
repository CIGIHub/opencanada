# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('core', '0022_auto_20151016_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('include_badge_in_main_feed', models.BooleanField(default=False)),
                ('badge_text', models.CharField(default='', max_length=60, blank=True)),
                ('badge_link', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailcore.Page', null=True)),
                ('featured_item', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailcore.Page', null=True)),
            ],
        ),
    ]
