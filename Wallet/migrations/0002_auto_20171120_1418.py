# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0001_initial'),
        ('Wallet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='user',
        ),
        migrations.AddField(
            model_name='wallet',
            name='user_profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UserAccount.UserProfile'),
        ),
    ]
