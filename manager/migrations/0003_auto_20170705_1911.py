# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-05 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20170703_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank_accounts',
            name='Transactions',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='manager.transactions'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='categories',
            field=models.CharField(blank=True, choices=[('Unapproved', 'Unapproved'), ('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='classifications',
            field=models.CharField(blank=True, choices=[('Cheque', 'Cheque'), ('Cash', 'Cash')], default='Cash', max_length=30),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='trans_type',
            field=models.CharField(blank=True, choices=[('out_trans', 'out_trans'), ('in_trans', 'in_trans')], max_length=20),
        ),
    ]