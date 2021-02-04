from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from db import db
from app import app 

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    return render_template("index.html")

@app.context_processor
def utility_processor():
    def get_categories():
        sql = "SELECT id, name FROM categories"
        result = db.session.execute(sql)
        categories = result.fetchall()
        return categories
    return dict(get_categories=get_categories)

# Individual category page
@app.route("/category/<int:id>")
def category(id):
    sql = "SELECT name FROM categories WHERE id=:cid"
    result = db.session.execute(sql, {"cid":id})
    category = result.fetchall()[0][0]

    sql = "SELECT name,id FROM items " \
          "WHERE category_id=:id"
    result = db.session.execute(sql, {"id":id})
    items = result.fetchall()
    return render_template("category.html", category=category, items=items)

@app.route("/item/<int:id>")
def item(id):
    sql = "SELECT * FROM items WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    # TODO: checkaa onko visible; jos False, heitä error-pagelle
    item = result.fetchall()[0]
    item_name = item[2]
    date_added = str(item[3])[:16]
    
    sql = "SELECT * FROM iteminfo WHERE item_id=:id"
    result = db.session.execute(sql, {"id":id})
    item_info = result.fetchall()[0]
    user_id = item_info[2]
    price = item_info[3]
    kuvaus = item_info[4]
    ostetaan = item_info[5]
    picture = item_info[6]

    return render_template("item.html", item_name=item_name, date_added=date_added, 
                            price=price, kuvaus=kuvaus, picture=picture)

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
    hashed = generate_password_hash(password)
    sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    db.session.execute(sql, {"username":username,"password":hashed})
    db.session.commit()

    session["username"] = username
    # TODO: use sessions to redirect back to the page they were on
    return redirect("/")

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
        print("SUCCESS")
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
    new = request.form["name_of_category"]
    sql = "INSERT INTO categories (name) VALUES (:new)"
    db.session.execute(sql, {"new":new})
    db.session.commit()
    return redirect("/admin")

@app.route("/profile")
def profile():
    # TODO!!
    return render_template("profile.html")

@app.route("/editads")
def editads():
    # TODO
    # Sivu, jolla voit lisätä ja muokata ilmoituksiasi
    return render_template("editads.html")