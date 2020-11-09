import json
from unittest import mock

from django.test import TestCase

from breakingbadapi_task.models import Character
from breakingbadapi_task.utils import (get_character_data_from_external_api,
                                       load_character_data_from_external_api)


class CharacterDataRetrievalTests(TestCase):
    @mock.patch("breakingbadapi_task.utils.requests.get")
    def test_character_data_retrieval_from_external_api(self, get_mock):
        sample_filename = "src/breakingbadapi_task/fixtures/character_sample.json"
        m = mock.MagicMock()
        m.json.return_value = json.load(open(sample_filename))
        get_mock.return_value = m

        characters = get_character_data_from_external_api()
        self.assertEqual(len(characters), 4)
        self.assertEqual(characters[0]["name"], "Walter White")
        self.assertEqual(characters[0]["status"], "Presumed dead")
        self.assertEqual(characters[0]["birthday"], "09-07-1958")

    @mock.patch("breakingbadapi_task.utils.requests.get")
    def test_character_data_loading_from_external_api(self, get_mock):
        sample_filename = "src/breakingbadapi_task/fixtures/character_sample.json"
        m = mock.MagicMock()
        m.json.return_value = json.load(open(sample_filename))
        get_mock.return_value = m

        load_character_data_from_external_api()
        self.assertEqual(Character.objects.count(), 4)

        first_character = Character.objects.first()
        self.assertEqual(first_character.name, "Walter White")
        self.assertEqual(first_character.status, "Presumed dead")
        self.assertEqual(str(first_character.birthday), "1958-09-07")
