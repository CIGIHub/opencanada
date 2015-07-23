# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('newsletter', '0006_auto_20150723_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField(verbose_name='Issue Date')),
                ('location', models.CharField(max_length=255)),
                ('event_link', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EventOrganizationLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(max_length=255)),
                ('logo', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsletterEventLink',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='newsletter.Event')),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('page', modelcluster.fields.ParentalKey(related_name='event', to='newsletter.NewsletterPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('newsletter.event', models.Model),
        ),
        migrations.AddField(
            model_name='eventorganizationlink',
            name='events',
            field=modelcluster.fields.ParentalKey(related_name='organization_link', to='newsletter.Event'),
        ),
        migrations.AddField(
            model_name='eventorganizationlink',
            name='organization',
            field=models.ForeignKey(related_name='event_links', to='newsletter.Organization'),
        ),
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='newsletter.Organization', null=True),
        ),
    ]
