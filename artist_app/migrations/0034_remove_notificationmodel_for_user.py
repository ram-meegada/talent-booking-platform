# Generated by Django 4.2.13 on 2024-05-16 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0033_alter_talentdetailsmodel_eye_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationmodel',
            name='for_user',
        ),
    ]
