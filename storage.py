import pyrebase

config = {
  'apiKey': "AIzaSyCrTOka75SikkOR4pNA2Da999x0QPBfdg4",
  'authDomain': "soc-radio-f3953.firebaseapp.com",
  'projectId': "soc-radio-f3953",
  'storageBucket': "soc-radio-f3953.appspot.com",
  'messagingSenderId': "533854826784",
  'appId': "1:533854826784:web:87df494b5a2ecab4526745"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# charGameID = "058"
# icon = storage.child("Icons").child(f"dev{charGameID}.png").get_url(None)
# print(icon)