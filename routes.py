from flask import render_template
from app import app 

from utils import utility_processor

import auth
import items 
import admin
import ad_controls

@app.route("/")
def index():
    itms = items.get_newest()
    return render_template("index.html", items=itms)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="404")