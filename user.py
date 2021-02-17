from flask import render_template, redirect, request, session
from db import db
from app import app
from file_management import upload_picture

# User operations; mostly adding ads

@app.route("/profile")
def profile():
    # TODO!!
    return render_template("profile.html")

@app.route("/add_ad")
def edit_ads():
    return render_template("add_ad.html")

@app.route("/upload_ad", methods=["POST"])
def make_ad():
    name = request.form["name"]
    category = request.form["category"]
    kuvaus = request.form["kuvaus"]
    hinta = int(request.form["hinta"].replace(" ",""))

    picture = request.files['picture']
    pic_name = upload_picture(picture)

    sql_c = "SELECT id FROM users WHERE username=:name"
    user_id = db.session.execute(sql_c, {"name":session["username"]}).fetchone()[0]

    sql_a = "INSERT INTO items (category_id, name, date_added, visible, user_id, price, kuvaus, picture)" \
            "VALUES (:category, :name, NOW(), TRUE, :user_id, :price, :kuvaus, :picture) RETURNING id"
    result_a = db.session.execute(sql_a, {"category":category,"name":name, "user_id":user_id, "price":hinta, "kuvaus":kuvaus,
                                          "picture":pic_name})
    db.session.commit()
    item_id = result_a.fetchone()[0]

    return redirect("/item/"+str(item_id))