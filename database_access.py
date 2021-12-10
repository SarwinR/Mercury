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

'''
data = {
    epic_id,
    display_name,
}
'''
def set_link_discord2fortnite(discord_id, data):
    global db
    profile_ref = db.collection("linkedIDs").document(str(discord_id))
    profile_ref.set(data)

def check_if_already_registered(discord_id):
    global db
    profile_ref = db.collection("linkedIDs").document(str(discord_id))
    profile = profile_ref.get()
    
    return profile.exists

def delete_user_details(discord_id):
    db.collection("linkedIDs").document(str(discord_id)).delete()
