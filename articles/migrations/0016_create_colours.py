# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_colours(apps, schema_editor):
    Colour = apps.get_model("articles", "Colour")

    Colour.objects.create(
        name="Black",
        rgb_value="#000000"
    )

    Colour.objects.create(
        name="White",
        rgb_value="#FFFFFF"
    )



class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0015_auto_20150715_1553'),
    ]

    operations = [
        migrations.RunPython(create_colours),
    ]
