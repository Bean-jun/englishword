# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordtable',
            name='use_num',
            field=models.IntegerField(default=0),
        ),
    ]
