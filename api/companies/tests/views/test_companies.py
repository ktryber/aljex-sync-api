import json
from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from companies.tests.factories import fake, UserFactory, CompanyUserFactory


class CompaniesAPITestCase(APITestCase):
    @mock.patch('companies.serializers.CompanyService')
    def test_create_company_and_user(self, MockCompanyService):
        company_user = CompanyUserFactory()
        MockCompanyService.create_company_and_user.return_value = (
            company_user.company, company_user.user
        )

        company_data = {
            "name": fake.company(),
            "street_address_1": fake.street_address(),
            "street_address_2": "",
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip": fake.zipcode(),
            "dot_number": "",
            "mc_number": "",
        }
        user_stub = UserFactory.stub()
        user_data = {
            "first_name": user_stub.first_name,
            "last_name": user_stub.last_name,
            "username": user_stub.username,
            "password_": "unsafe-password-here",
        }

        url = reverse('companies:company-create')
        data = {
            "company": company_data,
            "user": user_data,
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MockCompanyService.create_company_and_user.called)

    def test_retrieve_update(self):
        company_user = CompanyUserFactory()

        self.client.force_authenticate(company_user.user)

        url = reverse('companies:company-detail', kwargs={'pk': company_user.company.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test non-admin
        response = self.client.patch(
            url, data=json.dumps({"name": fake.company()}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Make an admin do it
        company_user.is_admin = True
        company_user.save()

        response = self.client.patch(
            url, data=json.dumps({"name": fake.company()}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UsersAPITestCase(APITestCase):
    def test_retrieve_update(self):
        company_user = CompanyUserFactory()

        self.client.force_authenticate(company_user.user)

        url = reverse('companies:user-detail', kwargs={'pk': company_user.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            url, data=json.dumps({"first_name": "bob"}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
