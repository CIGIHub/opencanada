# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_themes(apps, schema_editor):
    Theme = apps.get_model("themes", "Theme")

    default_theme = Theme.objects.get(is_default=True)

    HomePage = apps.get_model('core', 'HomePage')
    home, created = HomePage.objects.get_or_create(
        slug="home"
    )

    home.theme_id = default_theme.id
    home.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_set_contact_email'),
        ('themes', '0006_create_themes'),
    ]

    operations = [
        migrations.RunPython(set_themes),
    ]
