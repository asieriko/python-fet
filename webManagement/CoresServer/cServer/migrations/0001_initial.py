# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('fetfile', models.FileField(upload_to='fetfiles/')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfile', models.FileField(upload_to='results/')),
                ('tfile', models.FileField(upload_to='results/')),
                ('time', models.IntegerField()),
                ('fetfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cServer.File')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=False)),
                ('computer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cServer.Computer')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='fetfile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cServer.File'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cServer.Thread'),
        ),
    ]
