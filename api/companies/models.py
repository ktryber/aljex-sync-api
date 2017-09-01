from django.conf import settings
from django.db import models


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    external_key = models.CharField(max_length=128, unique=True)

    dot_number = models.CharField(max_length=15, blank=True)
    mc_number = models.CharField(max_length=15, blank=True)

    # Address info
    name = models.CharField(max_length=250)
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return '{0} <KEY: {1}>'.format(self.name, self.external_key or 'None')


class CompanyUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='company_user')
    company = models.ForeignKey('companies.Company', related_name='company_users')
    is_admin = models.BooleanField(default=False)
