# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-21 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopelectro', '0007_pages_data_migrations'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='in_stock',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
