# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('articles', '0086_articlepage_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriespage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='projects.ProjectPage', null=True),
        ),
    ]
