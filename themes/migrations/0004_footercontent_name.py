# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0003_theme_footer_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='footercontent',
            name='name',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]
