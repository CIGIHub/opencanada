# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0003_add_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributedDocument',
            fields=[
                ('document_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtaildocs.Document')),
                ('credit', models.CharField(default='', max_length=1024, blank=True)),
                ('source', models.CharField(default='', max_length=1024, blank=True)),
                ('usage_restrictions', models.TextField(default='', blank=True)),
            ],
            bases=('wagtaildocs.document',),
        ),
    ]
