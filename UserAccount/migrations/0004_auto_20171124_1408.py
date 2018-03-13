# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 14:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0003_tutor_searchable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='tags',
            field=models.ManyToManyField(blank=True, to='UserAccount.Tag'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UserAccount.University'),
        ),
    ]
