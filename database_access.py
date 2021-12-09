import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os
import base64
import json

db = None

def initialize_database():
    db_key_str= base64.b64decode(os.getenv('MERCURY_DB'))
    db_key_json = json.loads(db_key_str)

    cred = credentials.Certificate(db_key_json)
    firebase_admin.initialize_app(cred)

    global db
    db = firestore.client()