from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from companies.services.auth import generate_user_tokens


class FirebaseObtainAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        payload = generate_user_tokens(user)
        return Response(payload)
