from flask import Flask
from apis import api
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api.init_app(app)

app.run(debug=True)