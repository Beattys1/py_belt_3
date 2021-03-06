# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.CharField(max_length=30)),
                ('quote', models.TextField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('quoteManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('alias', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=200)),
                ('dob', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('userManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maker', to='belt_3.User'),
        ),
        migrations.AddField(
            model_name='quote',
            name='favorite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liker', to='belt_3.User'),
        ),
    ]
