# Generated by Django 4.2.13 on 2024-05-15 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0026_alter_usermodel_profile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentdetailsmodel',
            name='services',
            field=models.JSONField(default=list),
        ),
    ]
