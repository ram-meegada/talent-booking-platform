# Generated by Django 4.2.11 on 2024-05-07 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0009_chatstoragemodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatsessionmodel',
            old_name='uuid',
            new_name='session_id',
        ),
    ]
