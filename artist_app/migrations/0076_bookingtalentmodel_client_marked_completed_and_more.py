# Generated by Django 4.2.13 on 2024-06-06 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0075_reviewandratingsmodel_best_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingtalentmodel',
            name='client_marked_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bookingtalentmodel',
            name='talent_marked_completed',
            field=models.BooleanField(default=False),
        ),
    ]
