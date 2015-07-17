# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_styles(apps, schema_editor):
    FeatureStyle = apps.get_model("articles", "FeatureStyle")

    FeatureStyle.objects.create(
        name="Single Column - Text Only",
        number_of_columns=1,
        number_of_rows=1,
        include_image=False,
        overlay_text=False
    )

    FeatureStyle.objects.create(
        name="Single Column - Text and Image",
        number_of_columns=1,
        number_of_rows=1,
        include_image=False,
        overlay_text=False
    )

    FeatureStyle.objects.create(
        name="Full Width - Text overlayed on image",
        number_of_columns=3,
        number_of_rows=1,
        include_image=True,
        overlay_text=True
    )

    FeatureStyle.objects.create(
        name="Full Width - Double Height - Text overlayed on image",
        number_of_columns=3,
        number_of_rows=2,
        include_image=True,
        overlay_text=True
    )


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_auto_20150716_2116'),
    ]

    operations = [
        migrations.RunPython(create_styles),
    ]
