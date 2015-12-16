# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_projectpage_name'),
        ('articles', '0085_articlepage_json_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleProjectLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', modelcluster.fields.ParentalKey(related_name='project_link', to='articles.ArticlePage')),
                ('project', models.ForeignKey(related_name='project_link', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='projects.ProjectPage', null=True)),
            ],
        ),
    ]
