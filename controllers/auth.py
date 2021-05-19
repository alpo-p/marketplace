from db_operations.items_db import get_newest
from db_operations.auth_db import *
from app import app
from flask import request, render_template, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from os import urandom

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = get_user_password(username)
    items = get_newest()
    success = "False"
    if user:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            success = "True"
            session["csrf_token"] = urandom(16).hex()
    return render_template("index.html", items=items, success=success)

@app.route("/logout")
def logout():
    if not get_user_id():
        return render_template("error.html", message="Et ole kirjautuneena sisään!")
    else:
        del session["username"]
        return redirect("/")

@app.route("/register_screen")
def register_screen():
    if not get_user_id():
        return render_template("register_screen.html")
    else:
        return render_template("error.html", message="Olet jo kirjautuneena sisään!")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    sposti = request.form["sposti"]
    password = request.form["password"]
    puhelinnumero = request.form["puhelinnumero"]
    paikkakunta = request.form["paikkakunta"]
    kuvaus = request.form["kuvaus"]

    all_usernames = get_all_usernames()
    for name in all_usernames:
        if username == name[0]:
            return render_template("error.html", message="Tämä käyttäjätunnus on jo käytössä!")

    all_emails = get_all_emails()
    for mail in all_emails:
        if sposti == mail[0]:
            return render_template("error.html", message="Tämä sähköposti on jo käytössä!")
        
    hashed_pwd = generate_password_hash(password)

    user_id = create_auth_user(username, hashed_pwd)

    insert_user_info_to_db(sposti, puhelinnumero, paikkakunta, kuvaus, user_id)

    session["csrf_token"] = urandom(16).hex()
    session["username"] = username
    
    return redirect("/")

@app.route("/lost_pwd")
def lost_pwd():
    return render_template("error.html", message="Valitettavasti emme voi auttaa, luo uusi tunnus")
