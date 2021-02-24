from app import app
from flask import render_template, redirect, request, session
from werkzeug.security import check_password_hash
from db import db
from os import urandom

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/login", methods=["POST"])
def admin_login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM admin WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    admin = result.fetchone()
    if admin and check_password_hash(admin[0],password):
        session["admin_token"] = urandom(16).hex()
        session["admin"] = username
    else:
        print("ERROR")
    return redirect("/admin")

@app.route("/admin/logout")
def admin_logout():
    del session["admin"]
    return redirect("/")

@app.route("/admin/new_category", methods=["POST"])
def new_category():
    try:
        session["admin"]
    except:
        return redirect("/")
    if session["admin_token"] != request.form["admin_token"]: 
        return False
    new = request.form["name_of_category"]
    sql = "INSERT INTO categories (name) VALUES (:new)"
    db.session.execute(sql, {"new":new})
    db.session.commit()
    return redirect("/admin")