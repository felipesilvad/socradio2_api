# server.py
from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import threading

cred = credentials.Certificate("./firebaseKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
CORS(app)

docs = (
  db.collection("songs")
  # .where('timeslots', 'array_contains', '3 AM (EST)')
  .stream()
)

playlist = []
for doc in docs:
  playlist.append({'id': doc.id, 'secs': doc.to_dict()['secs'], 'title': doc.to_dict()['title']})
  
currentSongIndex = 0
currentSong = playlist[currentSongIndex]
now = datetime.now()

def changeSong():
  global currentSongIndex
  timer = threading.Timer(currentSong['secs'], changeSong)
  timer.start()
  currentSongIndex = currentSongIndex+1

changeSong()

@app.get('/getCurrentSong')
def getCurrentSong():
  print({"id":currentSong['id'], "timeStart": now, "title":currentSong['title']})
  return {"id":currentSong['id'], "timeStart": now, "title":currentSong['title']}

if __name__ == "__main__":
  getCurrentSong()
  # app.run(debug=True)
