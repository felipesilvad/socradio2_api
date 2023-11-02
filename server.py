from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import threading

cred = credentials.Certificate("./firebaseKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
CORS(app)

docs = (
  db.collection("songs")
  .where('main', '==', True)
  .stream()
)

playlist = []
for doc in docs:
  song = doc.to_dict()
  playlist.append({"id":doc.id, "data":song})
  
currentSongIndex = -1
currentSong = None

def changeSong():
  global currentSongIndex, currentSong
  currentSongIndex += 1

  if currentSongIndex == len(playlist):
    currentSongIndex = 0

  # currentSong = playlist[currentSongIndex]
  # currentSong['startTime'] = time.time()
  # currentSong['index'] = currentSongIndex

  currentSong = {"index":currentSongIndex, 
                 "startTime": time.time(),
                 "secs":playlist[currentSongIndex]["data"]["secs"]
                 }

  print("\n")
  print("--MAIN--")
  print("Starting song: ", currentSong)
  print("Next song in ", currentSong["secs"] , " seconds")

  timer = threading.Timer(currentSong["secs"], changeSong)
  timer.start()

@app.get('/currentSongMain')
def getCurrentSong():
  global currentSong
  return currentSong

@app.get('/playlistMain')
def getPlaylist():
  global playlist
  return playlist

docsChill = (
  db.collection("songs")
  # .where('timeslots', 'array_contains', '3 AM (EST)')
  .where('lv', '<', 3)
  .stream()

)

playlistChill = []
for doc in docsChill:
  song = doc.to_dict()
  playlistChill.append({"id":doc.id, "data":song})
  
currentSongChillIndex = -1
currentSongChill = None

def changeSongChill():
  global currentSongChillIndex, currentSongChill
  currentSongChillIndex += 1

  if currentSongChillIndex == len(playlistChill):
    currentSongChillIndex = 0

  # currentSongChill = playlistChill[currentSongChillIndex]
  # currentSongChill['startTime'] = time.time()
  # currentSongChill['index'] = currentSongChillIndex

  currentSongChill = {"index":currentSongChillIndex, 
                 "startTime": time.time(),
                 "secs":playlistChill[currentSongChillIndex]["data"]["secs"]
                 }

  print("\n")
  print("--Chill--")
  print("Starting song: ", currentSongChill)
  print("Next song in ", currentSongChill["secs"] , " seconds")

  timer = threading.Timer(currentSongChill["secs"], changeSongChill)
  timer.start()

@app.get('/currentSongChill')
def getCurrentSongChill():
  global currentSongChill
  return currentSongChill

@app.get('/playlistChill')
def getPlaylistChill():
  global playlistChill
  return playlistChill

if __name__ == "__main__":
  changeSong()
  changeSongChill()
  app.run(debug=True)
