from unittest import mock

from django.test import TestCase
from faker import Faker

from companies.services.company import CompanyService
from companies.tests.factories import UserFactory

fake = Faker()

PUSH_BASE = 0


class CompanyServiceTestCase(TestCase):
    def setUp(self):
        self.firebase_db_patcher = mock.patch('companies.services.company.firebase_db')
        self.firebase_db_mock = self.firebase_db_patcher.start()

        class A(object):
            pass

        class PushKey(object):
            @classmethod
            def push(self):
                global PUSH_BASE
                o = A()
                o.key = "some-key{0}".format(PUSH_BASE)
                PUSH_BASE += 1
                return o

            @classmethod
            def update(cls, *args):
                pass

        self.firebase_db_mock.reference.return_value = PushKey

    def tearDown(self):
        self.firebase_db_patcher.stop()

    def test_create_company(self):
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

        company = CompanyService.create_company(company_data)
        self.assertIsNotNone(company)
        self.assertTrue(self.firebase_db_mock.reference.called)

    def test_create_company_and_user(self):
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
        company, user = CompanyService.create_company_and_user(company_data, user_data)
        self.assertIsNotNone(company)
        self.assertTrue(self.firebase_db_mock.reference.called)
        self.assertIsNotNone(user)
        self.assertTrue(user.has_usable_password())
        self.assertIsNotNone(user.company_user)
