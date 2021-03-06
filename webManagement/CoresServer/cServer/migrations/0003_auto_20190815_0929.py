# Generated by Django 2.2.4 on 2019-08-15 09:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cServer', '0002_auto_20170827_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='computer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cServer.Computer'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cServer.Thread', unique=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='fetfile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cServer.File'),
        ),
    ]
