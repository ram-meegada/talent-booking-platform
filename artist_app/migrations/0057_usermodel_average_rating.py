# Generated by Django 4.2.13 on 2024-05-21 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0056_bookingtalentmodel_payment_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='average_rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True),
        ),
    ]
