import pyrebase
import os


config = {
 'apiKey': 'AIzaSyBWI48BhuBdKNQJsgeI3DmU8VKytGkvcsk',
  'authDomain': 'awsapi.firebaseapp.com',
  'databaseURL': 'https://awsapi.firebaseio.com',
  'storageBucket': 'awsapi.appspot.com',
  'serviceAccount': str(os.getcwd())+'\/awsapi.json'

}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
