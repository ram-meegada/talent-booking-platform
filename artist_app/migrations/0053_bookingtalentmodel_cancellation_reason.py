# Generated by Django 4.2.13 on 2024-05-20 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0052_reviewandratingsmodel_booking_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingtalentmodel',
            name='cancellation_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
