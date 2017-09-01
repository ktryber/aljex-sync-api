from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.firebase_admin import firebase_db


class HealthAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        # DB check
        get_user_model().objects.count()
        # Firebase check
        firebase_db.reference('appInfo').get()
        # Cache check
        cache.set('health', 1)
        cache.get('health')
        return Response({"status": "awesome"})
