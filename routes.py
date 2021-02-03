from flask import render_template, request, redirect
from app import app 

# https://www.w3schools.com/html/tryit.asp?filename=tryhtml_layout_flexbox
@app.route("/")
def index():
    return render_template("index.html")

# Individual category page
@app.route("/category/<int:id>")
def category(id):
    return render_template("category.html", id=id, items=items)