# Generated by Django 4.2.13 on 2024-05-13 05:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0015_alter_chatstoragemodel_timestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='name',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='chatstoragemodel',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 13, 11, 28, 43, 123932)),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='role',
            field=models.IntegerField(blank=True, choices=[(1, 'CLIENT'), (2, 'TALENT'), (3, 'ADMIN')], null=True),
        ),
    ]
