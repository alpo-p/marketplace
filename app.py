from flask import Flask
from os import getenv

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

import routes