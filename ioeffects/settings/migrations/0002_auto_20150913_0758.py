# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effect',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='twitter',
            name='modifier',
            field=models.DecimalField(default=0.0, max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='twitter',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
