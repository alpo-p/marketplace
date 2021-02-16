from app import app
from flask import request, render_template, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql,{"username":username})
    user = result.fetchone()
    if not user:
        # TODO invalid user
        pass
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            # TODO ilmoita käyttäjälle että kirjautunut
        else:
            # TODO invalid pass
            pass

    # TODO: use sessions to redirect back to the page they were on
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/login_screen")
def login_screen():
    return render_template("login_screen.html")

@app.route("/register_screen")
def register_screen():
    return render_template("register_screen.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    puhelinnumero = request.form["puhelinnumero"]
    paikkakunta = request.form["paikkakunta"]
    sposti = request.form["sposti"]
    hashed_pwd = generate_password_hash(password)
    sql_a = "INSERT INTO users (username,password)" \
            "VALUES (:username,:password) RETURNING id"
    result_a = db.session.execute(sql_a, {"username":username,"password":hashed_pwd})
    db.session.commit()
    user_id = result_a.fetchone()[0]

    sql_b = "INSERT INTO userinfo (user_id,puhelinnumero,paikkakunta,sposti)" \
            "VALUES (:user_id,:puhelinnumero,:paikkakunta,:sposti)"
    db.session.execute(sql_b, {"user_id":user_id,"puhelinnumero":puhelinnumero,"paikkakunta":paikkakunta,"sposti":sposti})
    db.session.commit()

    session["username"] = username
    # TODO: use sessions to redirect back to the page they were on
    return redirect("/")