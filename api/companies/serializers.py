from django.contrib.auth import get_user_model
from rest_framework import serializers

from companies import models
from companies.services.company import CompanyService


class UserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(required=True)
    password_ = serializers.CharField(required=True, min_length=6, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username', 'password_',)


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username')
        read_only_fields = ('id', 'username')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = (
            'id', 'name',
            'street_address_1', 'street_address_2', 'city', 'state', 'zip',
            'dot_number', 'mc_number', 'external_key',
        )
        read_only_fields = ('id', 'external_key',)


class CompanyAndUserSerializer(serializers.Serializer):
    company = CompanySerializer(required=True)
    user = UserSerializer(required=True)

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        user_data = validated_data.pop('user')

        company, user = CompanyService.create_company_and_user(
            company_data, user_data,
        )
        return {
            "company": company,
            "user": user,
        }

