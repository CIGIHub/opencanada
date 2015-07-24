# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0008_auto_20150723_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsletterarticlelink',
            old_name='article_text',
            new_name='override_text',
        ),
    ]
