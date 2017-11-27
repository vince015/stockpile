# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-20 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockpile_app', '0002_auto_20171028_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='count',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='item',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specifics', to='stockpile_app.Item'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='transaction',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='stockpile_app.Transaction'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('N', 'new'), ('S', 'seen'), ('D', 'done'), ('C', 'cancel')], default='N', max_length=2),
        ),
    ]
