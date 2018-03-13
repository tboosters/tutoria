# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 10:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bookings', '0002_auto_20171120_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bookings.Coupon'),
        ),
    ]