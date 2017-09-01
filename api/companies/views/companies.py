from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from companies.models import Company
from companies.permissions import UserObjectPermission, CompanyObjectPermission
from companies.serializers import CompanyAndUserSerializer, BasicUserSerializer, CompanySerializer


class CompanyCreateAPIView(CreateAPIView):
    serializer_class = CompanyAndUserSerializer
    authentication_classes = []
    permission_classes = []


class CompanyRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated, CompanyObjectPermission,)
    queryset = Company.objects.all()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = BasicUserSerializer
    permission_classes = (IsAuthenticated, UserObjectPermission,)
    queryset = get_user_model().objects.all()
