import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from storage import storage

cred = credentials.Certificate("firebaseKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def AddSong():
  doc_ref = db.collection(u'songs')
  doc_ref.add({
    u'test': 'wow',
  })
  
AddSong()