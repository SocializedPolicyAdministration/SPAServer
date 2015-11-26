# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeyManager',
            fields=[
                ('phone', models.BigIntegerField(serialize=False, primary_key=True)),
                ('paillier_private', models.CharField(max_length=4096)),
                ('paillier_public', models.CharField(max_length=4096)),
                ('ope_key', models.CharField(max_length=4096)),
            ],
        ),
    ]
