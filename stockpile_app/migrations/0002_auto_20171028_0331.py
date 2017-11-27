# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-28 03:31
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockpile_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='item',
            name='stock',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]