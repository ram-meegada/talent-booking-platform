# Generated by Django 4.2.13 on 2024-05-18 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0042_remove_usermodel_nationality'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talentdetailsmodel',
            name='weight',
        ),
    ]
