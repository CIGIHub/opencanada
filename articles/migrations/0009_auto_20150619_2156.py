# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('articles', '0008_auto_20150619_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indeptharticlelink',
            name='image',
        ),
        migrations.RemoveField(
            model_name='indeptharticlelink',
            name='text',
        ),
        migrations.AddField(
            model_name='indeptharticlelink',
            name='override_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', help_text='This field is optional. If not provided, the image will be pulled from the article page automatically. This field allows you to override the automatic image.', null=True),
        ),
        migrations.AddField(
            model_name='indeptharticlelink',
            name='override_text',
            field=wagtail.wagtailcore.fields.RichTextField(default='', help_text='This field is optional. If not provided, the text will be pulled from the article page automatically. This field allows you to override the automatic text.', blank=True),
        ),
    ]
