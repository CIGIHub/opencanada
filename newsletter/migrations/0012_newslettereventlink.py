# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150728_1915'),
        ('newsletter', '0011_newsletterlistpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterEventLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('override_text', wagtail.wagtailcore.fields.RichTextField(default='', help_text='Text to describe this event.', blank=True)),
                ('event', models.ForeignKey(related_name='newsletter_links', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='events.EventPage', help_text='Link to an event', null=True)),
                ('newsletter', modelcluster.fields.ParentalKey(related_name='event_links', to='newsletter.NewsletterPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
