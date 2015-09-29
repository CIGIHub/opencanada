# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0060_auto_20150925_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='include_caption_in_footer',
            field=models.BooleanField(default=False, help_text='Check to display the image caption in the footer.', verbose_name='Show caption in footer'),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='include_caption_in_footer',
            field=models.BooleanField(default=False, help_text='Check to display the image caption in the footer.', verbose_name='Show caption in footer'),
        ),
    ]
