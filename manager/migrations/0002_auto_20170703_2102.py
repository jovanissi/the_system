# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-03 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='classifications',
            field=models.CharField(blank=True, choices=[('Cash', 'Cash'), ('Cheque', 'Cheque')], default='Cash', max_length=30),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='trans_type',
            field=models.CharField(blank=True, choices=[('in_trans', 'in_trans'), ('out_trans', 'out_trans')], max_length=20),
        ),
    ]
