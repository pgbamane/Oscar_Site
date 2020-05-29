# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-13 17:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_final', '0003_update_email_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='email',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
