# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20150706_1526'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='main_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='images.AttributedImage', null=True),
        ),
        migrations.AlterField(
            model_name='indeptharticlelink',
            name='override_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='images.AttributedImage', help_text='This field is optional. If not provided, the image will be pulled from the article page automatically. This field allows you to override the automatic image.', null=True),
        ),
        migrations.AlterField(
            model_name='indepthpage',
            name='image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='images.AttributedImage', null=True),
        ),
    ]
