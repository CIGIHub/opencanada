# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_homepage_featured_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='FontStyle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('font_size', models.FloatField(default=1, help_text='The size of the fonts in ems.')),
                ('line_size', models.FloatField(default=100, help_text='The line height as a percentage.')),
                ('text_colour', models.CharField(default='#000000', help_text="The colour of the text in hexidecimal. For example, to get black enter '#000000'.", max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_item_font_style',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.FontStyle', null=True),
        ),
    ]
