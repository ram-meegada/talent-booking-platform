# Generated by Django 4.2.13 on 2024-05-22 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0057_usermodel_average_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactusmodel',
            name='data',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='contactusmodel',
            name='privacy_policy',
            field=models.TextField(default=''),
        ),
    ]
