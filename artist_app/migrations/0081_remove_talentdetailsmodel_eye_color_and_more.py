# Generated by Django 4.2.13 on 2024-06-11 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0080_colourpreferencesmodel_alter_permissionmodel_module'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talentdetailsmodel',
            name='eye_color',
        ),
        migrations.RemoveField(
            model_name='talentdetailsmodel',
            name='hair_color',
        ),
    ]
