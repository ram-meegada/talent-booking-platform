# Generated by Django 4.2.13 on 2024-06-07 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0077_alter_usermodel_average_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permissionmodel',
            name='can_add_edit',
        ),
        migrations.RemoveField(
            model_name='permissionmodel',
            name='can_be_delete',
        ),
        migrations.RemoveField(
            model_name='permissionmodel',
            name='can_view',
        ),
    ]
