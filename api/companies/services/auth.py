from firebase_admin import auth
from rest_framework.authtoken.models import Token

from libs.firebase_admin import app as firebase_app


def generate_firebase_user_token(user, api_token):
    if not hasattr(user, 'company_user'):
        return None

    additional_claims = {
        # store company ID
        'company_id': user.company_user.company.id,
        'company_key': user.company_user.company.external_key,
        'user_id': user.id,
        'user_email': user.username,
        'company_user_id': user.company_user.id,
        'api_token': api_token,
    }

    return auth.create_custom_token(
        str(user.id),
        developer_claims=additional_claims,
        app=firebase_app,
    )


def generate_user_tokens(user):
    token, created = Token.objects.get_or_create(user=user)
    firebase_token = generate_firebase_user_token(user=user, api_token=token.key)
    return {
        'api_token': token.key,
        'firebase_token': firebase_token.decode('utf-8'),
    }
