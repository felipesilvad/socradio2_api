import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from storage import storage
import audio_metadata
import os

cred = credentials.Certificate("firebaseKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def AddSong(filename):
  if ".ogg" in filename and ".sfl" not in filename:
    cover_file = filename.replace(".ogg", ".jpg")
    metadata = audio_metadata.load(filename)

    main = False
    if hasattr(metadata.tags, "main"):
      main = True
            
    storage.child(f"audios/{filename}").put(filename)
    audio_url = storage.child(f"audios/{filename}").get_url(None)
    
    storage.child(f"covers/{cover_file}").put(cover_file)
    cover_url = storage.child(f"covers/{cover_file}").get_url(None)
    
    doc_ref = db.collection(u'songs')
    doc_ref.add({
      u'album': metadata.tags.album[0],
      u'artist': metadata.tags.artist[0],
      u'title': metadata.tags.title[0],
      u'lv': int(metadata.tags.lv[0]),
      u'main': main,
      u'cover': cover_url,
      u'audio': audio_url,
      u'secs': metadata.streaminfo.duration,
    })
    print(metadata.tags.title[0], "Added")
  
def addAllSongs():
  directory = 'SongsToAdd'
  for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
      AddSong(f)
        
addAllSongs()