# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_projectpage_name'),
        ('articles', '0086_articleprojectlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleprojectlink',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articleprojectlink',
            name='project',
        ),
        migrations.AddField(
            model_name='articlepage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='projects.ProjectPage', null=True),
        ),
        migrations.DeleteModel(
            name='ArticleProjectLink',
        ),
    ]
