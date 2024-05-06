import firebase_admin
from firebase_admin import credentials

# Set up firestore authentication
cred = credentials.Certificate("mods/firestore-key.json")
db = firebase_admin.initialize_app(cred, 'my_app')

# Set up firestore connection 
db = app.client()

