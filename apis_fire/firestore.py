import pyrebase  ############package for interacting with firebase realtime database
import os  ############### to get

################setup configuration for the app
config = {
 'apiKey': "<apikey>",
    'authDomain': "awsapp-6bf1a.firebaseapp.com",
    'databaseURL': "https://awsapp-6bf1a.firebaseio.com",
    'projectId': "awsapp-6bf1a",
    'storageBucket': "awsapp-6bf1a.appspot.com",
  'serviceAccount': str(os.getcwd())+'/awsapi.json'

}

firebase = pyrebase.initialize_app(config)

########## initialize the db
db = firebase.database() 
