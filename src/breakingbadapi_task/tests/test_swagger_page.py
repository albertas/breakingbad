from django.test import TestCase
from django.urls import reverse


class SwaggerPageTests(TestCase):
    def test_swagger_ui_page(self):
        resp = self.client.get(reverse("swagger"))
        self.assertEqual(resp.status_code, 200)
