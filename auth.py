from app import app
from flask import request, render_template, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from items import get_newest

def get_user_id():
    try:
        username = session["username"]
    except:
        return False

    return username

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql,{"username":username})
    user = result.fetchone()
    items = get_newest() 
    if not user:
        success = "False"
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            success = "True"
        else:
            success = "False"
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
    all_usernames = db.session.execute("SELECT username FROM users").fetchall()
    for name in all_usernames:
        if username == name[0]:
            return render_template("error.html", message="Tämä käyttäjätunnus on jo käytössä!")

    sposti = request.form["sposti"]
    all_emails = db.session.execute("SELECT sposti FROM userinfo").fetchall()
    for mail in all_emails:
        if sposti == mail[0]:
            return render_template("error.html", message="Tämä sähköposti on jo käytössä!")
        
    password = request.form["password"]
    puhelinnumero = request.form["puhelinnumero"]
    paikkakunta = request.form["paikkakunta"]
    kuvaus = request.form["kuvaus"]
    hashed_pwd = generate_password_hash(password)
    sql_a = "INSERT INTO users (username,password)" \
            "VALUES (:username,:password) RETURNING id"
    result_a = db.session.execute(sql_a, {"username":username,"password":hashed_pwd})
    db.session.commit()
    user_id = result_a.fetchone()[0]

    sql_b = "INSERT INTO userinfo (user_id,puhelinnumero,paikkakunta,sposti, kuvaus)" \
            "VALUES (:user_id,:puhelinnumero,:paikkakunta,:sposti,:kuvaus)"
    db.session.execute(sql_b, 
        {"user_id":user_id,"puhelinnumero":puhelinnumero,"paikkakunta":paikkakunta,"sposti":sposti,"kuvaus":kuvaus})
    db.session.commit()

    session["username"] = username
    
    return redirect("/")

@app.route("/lost_pwd")
def lost_pwd():
    return render_template("error.html", message="Valitettavasti emme voi auttaa, luo uusi tunnus")
