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
  song = doc.to_dict()
  playlist.append(song)
  
currentSongIndex = -1
currentSong = {}

def changeSong(currentSongIndex, currentSong):
  currentSongIndex += 1
  currentSong = playlist[currentSongIndex]
  # currentSong.startTime = datetime.now()

  print("New song index: ", currentSongIndex)
  print("Starting song: ", currentSong)
  print("Next song in ", currentSong["secs"] , " seconds")

  timer = threading.Timer(currentSong["secs"], changeSong, [currentSongIndex, currentSong])
  timer.start()

changeSong(currentSongIndex, currentSong)

@app.get('/currentSong')
def getCurrentSong():
  return currentSong

if __name__ == "__main__":
  # getCurrentSong()
  app.run(debug=True)
