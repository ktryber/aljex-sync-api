import json
from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from companies.tests.factories import fake, UserFactory, CompanyUserFactory


class CompaniesAPITestCase(APITestCase):

    @mock.patch('companies.views.auth.generate_user_tokens')
    def test_create_company_and_user(self, mock_generate_user_tokens):
        company_user = CompanyUserFactory()

        mock_generate_user_tokens.return_value = {
            "api_token": "some-key",
            "firebase_token": "some-key",
        }

        url = reverse('companies:api-auth-token')

        company_user.user.set_password("badpassword")
        company_user.user.save()

        response = self.client.post(url, data=json.dumps({
            "username": company_user.user.username,
            "password": "badpassword",
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # UPPER CASE
        response = self.client.post(url, data=json.dumps({
            "username": company_user.user.username.upper(),
            "password": "badpassword",
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # LOWER CASE
        response = self.client.post(url, data=json.dumps({
            "username": company_user.user.username.lower(),
            "password": "badpassword",
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
