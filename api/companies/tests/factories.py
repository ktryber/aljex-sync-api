import factory
import factory.django
from django.contrib.auth import get_user_model
from faker import Faker

from companies import models

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'agent{0}{1}'.format(n, fake.email()))
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Company

    name = factory.LazyAttribute(lambda x: fake.company())
    external_key = factory.Sequence(lambda n: "{0:0>100}".format(n))
    street_address_1 = factory.LazyAttribute(lambda x: fake.street_address())
    street_address_2 = ""
    city = factory.LazyAttribute(lambda x: fake.city())
    state = factory.LazyAttribute(lambda x: fake.state_abbr())
    zip = factory.LazyAttribute(lambda x: fake.zipcode())


class CompanyUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CompanyUser

    company = factory.SubFactory(CompanyFactory)
    user = factory.SubFactory(UserFactory)
