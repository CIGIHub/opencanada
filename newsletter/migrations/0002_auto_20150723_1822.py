# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletterpage',
            name='issue_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Issue Date'),
        ),
    ]
