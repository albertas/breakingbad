import requests


def get_character_data_from_external_api():
    url = "https://breakingbadapi.com/api/characters"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
