from db_operations.items_db import get_newest
from flask import render_template
from app import app 

from utils import utility_processor

## These are imported routes
import controllers.auth
import controllers.items
import controllers.ad_controls
import controllers.admin

@app.route("/")
def index():
    itms = get_newest()
    return render_template("index.html", items=itms)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="404")