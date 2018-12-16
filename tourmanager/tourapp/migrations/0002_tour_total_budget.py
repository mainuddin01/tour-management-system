# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-03 06:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='total_budget',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
            preserve_default=False,
        ),
    ]
