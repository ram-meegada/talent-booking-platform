# Generated by Django 4.2.13 on 2024-05-20 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0055_manageaddressmodel_city_manageaddressmodel_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingtalentmodel',
            name='payment_completed',
            field=models.BooleanField(default=False),
        ),
    ]
