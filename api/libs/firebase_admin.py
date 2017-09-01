import firebase_admin
from django.conf import settings
from firebase_admin import credentials
from firebase_admin import db as firebase_db

# NOTE: we are phasing out usage of Pyrebase. there are currently 2 differnet Firebase clients

cred = credentials.Certificate(settings.FIREBASE_CONFIG['serviceAccount'])
app = firebase_admin.initialize_app(cred, {'databaseURL': settings.FIREBASE_CONFIG['databaseURL']})
