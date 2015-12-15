# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0021_themecontent_json_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twitteratimember',
            name='category',
        ),
        migrations.DeleteModel(
            name='TwitteratiMember',
        ),
        migrations.DeleteModel(
            name='TwitteratiMemberCategory',
        ),
    ]
