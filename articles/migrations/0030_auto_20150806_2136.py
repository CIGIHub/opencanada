# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.core.blocks
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0029_auto_20150811_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapteredarticlepage',
            name='end_notes',
            field=wagtail.core.fields.StreamField([('end_note', wagtail.core.blocks.StructBlock([(b'identifier', wagtail.core.blocks.CharBlock()), (b'text', wagtail.core.blocks.TextBlock())]))], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chapteredarticlepage',
            name='works_cited',
            field=wagtail.core.fields.StreamField([('citation', wagtail.core.blocks.StructBlock([(b'text', wagtail.core.blocks.TextBlock())]))], null=True, blank=True),
        ),
    ]
