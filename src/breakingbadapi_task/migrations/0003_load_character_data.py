from django.db import migrations

from breakingbadapi_task.utils import load_character_data_from_external_api


def load_character_data(apps, schema_editor):
    Character = apps.get_model("breakingbadapi_task", "Character")
    Occupation = apps.get_model("breakingbadapi_task", "Occupation")

    load_character_data_from_external_api(Character, Occupation)


class Migration(migrations.Migration):

    dependencies = [
        ("breakingbadapi_task", "0002_auto_20201107_1832"),
    ]

    operations = [
        migrations.RunPython(load_character_data, migrations.RunPython.noop),
    ]
