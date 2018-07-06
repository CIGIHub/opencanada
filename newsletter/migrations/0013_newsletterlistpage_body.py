# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0012_newslettereventlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletterlistpage',
            name='body',
            field=wagtail.core.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]
