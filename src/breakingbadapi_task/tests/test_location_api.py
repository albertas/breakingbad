from datetime import datetime
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from parameterized import parameterized
from pytz import timezone


@mock.patch(
    "breakingbadapi_task.models.timezone.now",
    return_value=datetime(2020, 1, 1, tzinfo=timezone(settings.TIME_ZONE)),
)
class LocationAPITests(TestCase):
    fixtures = ["characters.json", "locations.json"]

    def test_get_location_list(self, *args):
        resp = self.client.get(reverse("location-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json()) > 1)

    def test_get_location(self, *args):
        resp = self.client.get(reverse("location-detail", kwargs={"pk": "1"}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["character"], 1)
        self.assertEqual(resp.json()["character_name"], "Walter White")
        self.assertEqual(resp.json()["timestamp"], "2020-11-10T00:00:00Z")
        self.assertEqual(resp.json()["point"], "SRID=4326;POINT (0 0)")

    @parameterized.expand(
        [
            (
                {
                    "character": 2,
                    "point": "SRID=4326;POINT (0 0)",
                },
                {
                    "character": 2,
                    "timestamp": "2020-01-01T00:00:00Z",
                    "point": "SRID=4326;POINT (0 0)",
                },
            ),
            (
                {
                    "character": 1,
                    "timestamp": "2020-12-10T16:15:00Z",
                    "point": "SRID=4326;POINT (1.0 1.0)",
                },
                {
                    "character": 1,
                    "timestamp": "2020-12-10T16:15:00Z",
                    "point": "SRID=4326;POINT (1 1)",
                },
            ),
        ]
    )
    def test_create_location(self, now_mock, new_location_data, expected):
        url = reverse("location-detail", kwargs={"pk": "0"})
        resp = self.client.post(url, data=new_location_data)
        self.assertEqual(resp.status_code, 201)
        for key in expected:
            self.assertEqual(resp.json()[key], expected[key])

    def test_update_location(self, *args):
        url = reverse("location-detail", kwargs={"pk": "1"})
        updated_data = {
            "character": 2,
            "timestamp": "2020-12-10T16:15:00Z",
            "point": "SRID=4326;POINT (1 1)",
        }
        resp = self.client.patch(url, data=updated_data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["character"], updated_data["character"])
        self.assertEqual(resp.json()["timestamp"], updated_data["timestamp"])
        self.assertEqual(resp.json()["point"], updated_data["point"])

    def test_delete_location(self, *args):
        resp = self.client.delete(reverse("location-detail", kwargs={"pk": "1"}))
        self.assertEqual(resp.status_code, 204)

    def test_filters(self, *args):
        url = reverse("location-list")
        query = "&".join(["character=1", "timestamp=2020-11-10T00:00:00Z"])

        resp = self.client.get(f"{url}?{query}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)
        self.assertEqual(resp.json()[0]["character_name"], "Walter White")
