# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0013_newsletterlistpage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletterlistpage',
            name='intro_text',
            field=wagtail.wagtailcore.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]
