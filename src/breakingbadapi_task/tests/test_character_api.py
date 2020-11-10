from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class CharacterAPITests(TestCase):
    fixtures = ["characters.json"]

    def test_get_character_list(self):
        resp = self.client.get(reverse("character-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

    def test_get_character(self):
        resp = self.client.get(reverse("character-detail", kwargs={"pk": "1"}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["name"], "Walter White")
        self.assertEqual(resp.json()["birthday"], "1958-09-07")
        self.assertEqual(resp.json()["status"], "Presumed dead")

    def test_create_character(self):
        url = reverse("character-detail", kwargs={"pk": "0"})
        new_character_data = {
            "name": "Test Name",
            "birthday": "1960-01-01",
            "status": "Alive",
        }
        resp = self.client.post(url, data=new_character_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["id"], 4)
        self.assertEqual(resp.json()["name"], new_character_data["name"])
        self.assertEqual(resp.json()["birthday"], new_character_data["birthday"])
        self.assertEqual(resp.json()["status"], new_character_data["status"])

    def test_update_character(self):
        url = reverse("character-detail", kwargs={"pk": "1"})
        updated_data = {
            "name": "Test Name",
            "birthday": "1960-01-01",
            "status": "Alive",
        }
        resp = self.client.patch(url, data=updated_data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["name"], updated_data["name"])
        self.assertEqual(resp.json()["birthday"], updated_data["birthday"])
        self.assertEqual(resp.json()["status"], updated_data["status"])

    def test_delete_character(self):
        resp = self.client.delete(reverse("character-detail", kwargs={"pk": "1"}))
        self.assertEqual(resp.status_code, 204)

    def test_filters(self):
        url = reverse("character-list")
        query = "&".join(
            [
                "name=walter",
                "birthday=1958",
                "state=presumed dead",
                "occupation=king",
            ]
        )

        resp = self.client.get(f"{url}?{query}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]["name"], "Walter White")

    @parameterized.expand(
        [
            ("name", "1", ["Jesse Pinkman", "Skyler White", "Walter White"]),
            ("name", "0", ["Walter White", "Skyler White", "Jesse Pinkman"]),
            ("birthday", "1", ["1958-09-07", "1970-08-11", "1984-09-24"]),
            ("birthday", "0", ["1984-09-24", "1970-08-11", "1958-09-07"]),
        ]
    )
    def test_ordering(self, order_by, ascending, result):
        url = reverse("character-list")
        query = "&".join(
            [
                f"orderBy={order_by}",
                f"ascending={ascending}",
            ]
        )

        resp = self.client.get(f"{url}?{query}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

        for character_data, expected in zip(resp.json(), result):
            self.assertEqual(character_data.get(order_by), expected)
