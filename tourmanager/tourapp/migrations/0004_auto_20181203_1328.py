# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-03 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourapp', '0003_auto_20181203_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='tour',
            name='start_date',
            field=models.DateField(),
        ),
    ]