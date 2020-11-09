# Generated by Django 3.1.2 on 2020-11-08 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("breakingbadapi_task", "0003_load_character_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="occupation",
            name="character",
            field=models.ManyToManyField(
                related_name="occupation", to="breakingbadapi_task.Character"
            ),
        ),
    ]
