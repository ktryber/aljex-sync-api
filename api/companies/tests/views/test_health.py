from unittest import skipIf

from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


@skipIf(not settings.FIREBASE_ENABLED, "Firebase not enabled.")
class HealthAPITestCase(APITestCase):

    def test_health_endpoint(self):
        url = reverse('companies:health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
