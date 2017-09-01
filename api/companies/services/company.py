from django.contrib.auth import get_user_model
from django.db import transaction

from companies.models import Company, CompanyUser
from libs.firebase_admin import firebase_db

User = get_user_model()


class CompanyService(object):

    def __init__(self, company):
        self.company = company

    @transaction.atomic
    def add_user_to_company(self, user, is_admin=False):
        company_user = CompanyUser(
            user=user,
            company=self.company,
            is_admin=is_admin,
        )
        company_user.save()
        return company_user

    @classmethod
    @transaction.atomic
    def create_company(cls, company_data):
        updates = {}
        company_key = firebase_db.reference('companies').push().key

        company = Company(
            external_key=company_key,
            **company_data,
        )
        company.save()

        updates['companies/{key}/pk'.format(key=company_key)] = company.pk
        firebase_db.reference().update(updates)
        return company

    @classmethod
    @transaction.atomic
    def create_company_and_user(cls, company_data, user_data):
        company = cls.create_company(company_data)
        password_ = user_data.pop('password_')

        user = User(
            is_staff=False,
            is_superuser=False,
            is_active=True,
            **user_data
        )
        user.set_password(password_)
        user.save()

        cls(company=company).add_user_to_company(user, is_admin=True)

        return company, user
