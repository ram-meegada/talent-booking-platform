# Generated by Django 4.2.13 on 2024-05-20 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0053_bookingtalentmodel_cancellation_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentcategorymodel',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='artist_app.uploadmediamodel'),
        ),
    ]
