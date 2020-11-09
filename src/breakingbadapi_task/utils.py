from datetime import datetime

import requests

from breakingbadapi_task.models import Character, Occupation


def get_character_data_from_external_api():
    url = "https://breakingbadapi.com/api/characters"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def load_character_data_from_external_api(character_model=Character, occupation_model=Occupation):
    character_list = get_character_data_from_external_api()
    for character_data in character_list:
        data = {
            "name": character_data["name"],
            "status": character_data["status"],
        }

        if character_data["birthday"].lower() != "unknown":
            data["birthday"] = datetime.strptime(character_data["birthday"], "%m-%d-%Y")

        character = character_model.objects.create(**data)

        for occupation_title in character_data["occupation"]:
            obj, _ = occupation_model.objects.get_or_create(title=occupation_title)
            character.occupation.add(obj)
