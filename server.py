# server.py
from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import time

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

current_playlist = []

for doc in docs:
  current_playlist.append({'id': doc.id, 'secs': doc.to_dict()['secs']})

# def createToken():
#   grant = livekit.VideoGrant(room_join=True, room="My Cool Room")
#   token = livekit.AccessToken(os.environ.get("LK_API_KEY"), os.environ.get("LK_API_SECRET"), grant=grant, identity="bob", name="Bob")
#   print(token)

@app.get("/")
def home():
  return "SoC Radio"

@app.get('/getCurrentSong')
def getCurrentSong():
  # value = {}
  # for song in current_playlist:
  #   currentsongID = song['id']
  #   value = {"id":currentsongID,'startTime':datetime.now()}
  #   time.sleep(song['secs'])
  # return value
  now = datetime.now()
  return {"id":"lVAj1qbpABl2BMETNpWt", "timeStart": now}

if __name__ == "__main__":
  app.run(debug=True)
