from flask import render_template, redirect, request, session
from db import db
from app import app

'''
Stuff the users do themselves, such as edit their profile or sell/buy ads
'''

@app.route("/profile")
def profile():
    # TODO!!
    return render_template("profile.html")

@app.route("/my_ads")
def edit_ads():
    return render_template("my_ads.html")

@app.route("/make_ad", methods=["POST"])
def make_ad():
    name = request.form["name"]
    category = request.form["category"]
    ostetaan = request.form["ostetaan"]
    kuvaus = request.form["kuvaus"]
    hinta = request.form["hinta"]

    sql_a = "INSERT INTO items (category_id, name, date_added, visible)" \
            "VALUES (:category, :name, NOW(), TRUE) RETURNING id"
    result_a = db.session.execute(sql_a, {"category":category,"name":name})
    db.session.commit()
    item_id = result_a.fetchone()[0]

    sql_b = "INSERT INTO iteminfo (item_id, user_id, price, kuvaus, ostetaan)" \
            "VALUES (:item_id, :user_id, :price, :kuvaus, :ostetaan)"
    sql_c = "SELECT id FROM users WHERE username=:name"
    user_id = db.session.execute(sql_c, {"name":session["username"]}).fetchone()[0]
    db.session.execute(sql_b, {"item_id":item_id,"user_id":user_id,"price":hinta,"kuvaus":kuvaus,"ostetaan":ostetaan})
    db.session.commit()

    return redirect("/my_ads")