# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0061_auto_20150928_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='fullbleed_feature',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='externalarticlepage',
            name='fullbleed_feature',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='headline',
            name='fullbleed_feature',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seriespage',
            name='fullbleed_feature',
            field=models.BooleanField(default=False),
        ),
    ]
