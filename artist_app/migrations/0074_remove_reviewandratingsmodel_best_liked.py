# Generated by Django 5.0.4 on 2024-06-06 06:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("artist_app", "0073_alter_talentdetailsmodel_tags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reviewandratingsmodel",
            name="best_liked",
        ),
    ]
