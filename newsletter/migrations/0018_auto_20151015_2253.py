# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0017_auto_20151005_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletterarticlelink',
            name='article',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailcore.Page', help_text='Link to an internal article', null=True),
        ),
        migrations.AlterField(
            model_name='newslettereventlink',
            name='event',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='events.EventPage', help_text='Link to an event', null=True),
        ),
        migrations.AlterField(
            model_name='newsletterexternalarticlelink',
            name='external_article',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='articles.ExternalArticlePage', help_text='Link to an external article', null=True),
        ),
    ]
