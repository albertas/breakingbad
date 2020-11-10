from django.test import TestCase
from django.urls import reverse


class IndexAndSwaggerPageTests(TestCase):
    def test_swagger_ui_page(self):
        resp = self.client.get(reverse("swagger"))
        self.assertEqual(resp.status_code, 200)

    def test_index_page(self):
        resp = self.client.get(reverse("index"))
        self.assertEqual(resp.status_code, 302)
