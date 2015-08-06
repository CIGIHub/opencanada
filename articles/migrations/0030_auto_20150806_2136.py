# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0029_auto_20150805_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapteredarticlepage',
            name='end_notes',
            field=wagtail.wagtailcore.fields.StreamField([('end_note', wagtail.wagtailcore.blocks.StructBlock([(b'identifier', wagtail.wagtailcore.blocks.CharBlock()), (b'text', wagtail.wagtailcore.blocks.TextBlock())]))], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chapteredarticlepage',
            name='works_cited',
            field=wagtail.wagtailcore.fields.StreamField([('citation', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.TextBlock())]))], null=True, blank=True),
        ),
    ]
