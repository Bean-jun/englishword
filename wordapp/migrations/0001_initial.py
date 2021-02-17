# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WordTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('word', models.CharField(max_length=100)),
                ('trans', models.CharField(max_length=200)),
                ('use_num', models.IntegerField()),
            ],
        ),
    ]
