from django.conf.urls import url

from companies.views import companies
from companies.views import auth
from companies.views import health

urlpatterns = [
    url(r'^companies$',
        companies.CompanyCreateAPIView.as_view(), name='company-create'),
    url(r'^companies/(?P<pk>\d+)$',
        companies.CompanyRetrieveUpdateAPIView.as_view(), name='company-detail'),
    url(r'^users/(?P<pk>\d+)$',
        companies.UserRetrieveUpdateAPIView.as_view(), name='user-detail'),
    url(r'^health$',
        health.HealthAPIView.as_view(), name='health'),
    url(r'^api-auth-token$',
        auth.FirebaseObtainAuthTokenView.as_view(), name='api-auth-token'),
]
