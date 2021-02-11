from flask import render_template
from app import app 

from utils import utility_processor

import auth
import items 
import admin
import userops

@app.route("/")
def index():
    return render_template("index.html")
