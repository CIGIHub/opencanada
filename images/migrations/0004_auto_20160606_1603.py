# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20160405_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributedrendition',
            name='file',
            field=models.ImageField(height_field='height', width_field='width', upload_to=wagtail.images.models.get_rendition_upload_to),
        ),
    ]
