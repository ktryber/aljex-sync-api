from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from companies import models


@admin.register(models.CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    pass
