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
now = datetime.now()

timer = threading.Timer(getCurrentSong()['secs'], changeSong, [currentSongIndex])
timer.start()

def getCurrentSong():
  return playlist[currentSongIndex]

def changeSong(currentSongIndex):
  secs = getCurrentSong()['secs']
  currentSongIndex += 1
  currentSong = getCurrentSong()
  
  print("on changeSong - ",{"id":currentSong['id'], "timeStart": now, "title":currentSong['title']})
  timer = threading.Timer(secs, changeSong, [currentSongIndex])
  timer.start()

@app.get('/getCurrentSong')
def currentSong():
  return getCurrentSong()

if __name__ == "__main__":
  # getCurrentSong()
  app.run(debug=True)
