# Generated by Django 4.2.13 on 2024-05-13 11:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0020_alter_chatstoragemodel_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatstoragemodel',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 13, 17, 11, 58, 352525)),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='phone_no',
            field=models.CharField(default='', max_length=100),
        ),
    ]
