# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0017_twitteraticategory_twitteratiuser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TwitteratiUser',
            new_name='TwitteratiMember',
        ),
        migrations.RenameModel(
            old_name='TwitteratiCategory',
            new_name='TwitteratiMemberCategory',
        ),
    ]
