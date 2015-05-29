# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('core', '0003_remove_legacyarticlepage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='legacyarticlepage',
            name='page_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=0, serialize=False, to='wagtailcore.Page'),
            preserve_default=False,
        ),
    ]
