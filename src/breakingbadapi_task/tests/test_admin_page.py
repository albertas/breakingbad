from django.test import TestCase
from django.urls import reverse


class AdminPageTests(TestCase):
    def test_admin_page(self):
        resp = self.client.get(reverse("admin:index"))
        self.assertEqual(resp.status_code, 302)
