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
currentSong = None

def changeSong():
  global currentSongIndex, currentSong
  currentSongIndex += 1

  if currentSongIndex == len(playlist):
    currentSongIndex = 0

  currentSong = playlist[currentSongIndex]
  currentSong['startTime'] = time.time()

  print("\n")
  print("Starting song: ", currentSong)
  print("Next song in ", currentSong["secs"] , " seconds")

  timer = threading.Timer(currentSong["secs"], changeSong)
  timer.start()

@app.get('/currentSong')
def getCurrentSong():
  global currentSong
  return currentSong

if __name__ == "__main__":
  changeSong()
  app.run(debug=True)
