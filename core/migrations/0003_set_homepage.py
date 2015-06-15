# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_homepage(apps, schema_editor):
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model("core", "HomePage")
    homepage = HomePage.objects.get(slug="home")

    # Create default site
    Site.objects.create(
        hostname='localhost',
        root_page_id=homepage.id,
        is_default_site=True
    )

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_create_home_page'),
    ]

    operations = [
        migrations.RunPython(set_homepage),
    ]
