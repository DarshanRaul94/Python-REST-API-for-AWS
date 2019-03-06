from flask import Flask
from apis_fire import api
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api.init_app(app)

app.run(debug=True)
#app.run(debug=True,ssl_context='adhoc' ) ######to make this https
#pip install pyopenssl
