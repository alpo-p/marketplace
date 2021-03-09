from flask import render_template, redirect, request, session
from db import db
from app import app
from file_management import upload_picture
from auth import get_user_id
import re

@app.route("/add_ad")
def add_ad():
    if not get_user_id():
        return render_template("error.html", message="Et ole kirjautuneena sisään!")
    return render_template("add_ad.html")

@app.route("/upload_ad", methods=["POST"])
def make_ad():
    if session["csrf_token"] != request.form["csrf_token"]: 
        return False

    name = request.form["name"]
    category = request.form["category"]
    kuvaus = request.form["kuvaus"]
    hinta = request.form["hinta"]
    try:
        hinta = int(re.sub('[^0-9]','',hinta))
    except:
        return render_template("error.html", message="Hinnan täytyy olla numero")

    picture = request.files['picture']
    pic_name = upload_picture(picture)

    if len(name) > 50 or len(kuvaus) > 150 or hinta > 1000000000:
        return render_template("error.html", message="Liian pitkä rimpsu informaatiota!")

    user_id = get_user_id()
    if not user_id:
        return render_template("error.html", message="Et ole kirjautuneena sisään!")

    sql_a = "INSERT INTO items (category_id, name, date_added, visible, user_id, price, kuvaus, picture)" \
            "VALUES (:category, :name, NOW(), TRUE, :user_id, :price, :kuvaus, :picture) RETURNING id"
    result_a = db.session.execute(sql_a, {"category":category,"name":name, "user_id":user_id, "price":hinta, "kuvaus":kuvaus,
                                          "picture":pic_name})
    db.session.commit()
    item_id = result_a.fetchone()[0]

    return redirect("/item/"+str(item_id))

@app.route("/edit_ads")
def edit_ads():
    user_id = get_user_id()
    if not user_id:
        return render_template("error.html", message="Et ole kirjautuneena sisään!")
    sql = "SELECT * FROM items WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    items = result.fetchall()
    return render_template("edit_ads.html", items=items)

@app.route("/edit_ads/<int:id>")
def edit_single_ad(id):
    item_owner = db.session.execute("SELECT user_id from items WHERE id=:id", {"id":id}).fetchone()[0]
    if item_owner != get_user_id():
        return render_template("error.html", message="Et voi muokata tätä tuotetta, sillä et omista sitä!")
    sql = "SELECT * FROM items WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    item = result.fetchone()
    return render_template("edit_single_ad.html", item=item)

@app.route("/update_ad", methods=["POST"])
def update_ad():
    if session["csrf_token"] != request.form["csrf_token"]: 
        return False

    id = request.form["id"]

    item_owner = db.session.execute("SELECT user_id from items WHERE id=:id", {"id":id}).fetchone()[0]
    if item_owner != get_user_id():
        return render_template("error.html", message="Et voi muokata tätä tuotetta, sillä et omista sitä!")

    name = request.form["name"]
    hinta = request.form["hinta"]
    try:
        hinta = int(re.sub('[^0-9]','',hinta))
    except:
        return render_template("error.html", message="Hinnan täytyy olla numero")
    kuvaus = request.form["kuvaus"]

    if len(name) > 50 or len(kuvaus) > 150 or hinta > 1000000000:
        return render_template("error.html", message="Liian pitkä rimpsu informaatiota!")

    picture = request.files["picture"]
    if picture:
        pic_name = upload_picture(picture)
        sql = "UPDATE items SET name=:name, price=:price, kuvaus=:kuvaus, picture=:picture " \
              "WHERE id=:id"
        db.session.execute(sql, {"name":name,"price":hinta,"kuvaus":kuvaus,"picture":pic_name,"id":id})
    else:
        sql = "UPDATE items SET name=:name, price=:price, kuvaus=:kuvaus " \
              "WHERE id=:id"
        db.session.execute(sql, {"name":name,"price":hinta,"kuvaus":kuvaus,"id":id})
    db.session.commit()
    return redirect("/edit_ads")

@app.route("/delete_ad/<int:id>")
def delete_ad(id):
    item_owner = db.session.execute("SELECT user_id from items WHERE id=:id", {"id":id}).fetchone()[0]
    if item_owner != get_user_id():
        return render_template("error.html", message="Et voi poistaa tätä tuotetta, sillä et omista sitä!")
    sql = "DELETE FROM items WHERE id=:id"
    db.session.execute(sql,{"id":id})
    db.session.commit()
    return redirect("/edit_ads")
