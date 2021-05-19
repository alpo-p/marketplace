from db_operations.auth_db import get_user_id
from db_operations.ad_controls_db import *
from utils import parse_price
from flask import render_template, redirect, request, session
from app import app
from file_management import upload_picture

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
    picture = request.files['picture']

    try:
        hinta = parse_price(hinta) 
    except:
        return render_template("error.html", message="Hinnan täytyy olla numero")

    if len(name) > 50 or len(kuvaus) > 150 or hinta > 1000000000:
        return render_template("error.html", message="Liian pitkä rimpsu informaatiota!")

    pic_name = upload_picture(picture)

    user_id = get_user_id()
    if not user_id:
        return render_template("error.html", message="Et ole kirjautuneena sisään!")

    item_id = commit_new_ad_to_DB_and_return_item_id(category, name, user_id, hinta, kuvaus, pic_name)
    return redirect("/item/"+str(item_id))

@app.route("/edit_ads")
def edit_ads():
    user_id = get_user_id()
    if not user_id:
        return render_template("error.html", message="Et ole kirjautuneena sisään!")
    items = get_all_items_by_user_id(user_id)
    return render_template("edit_ads.html", items=items)

@app.route("/edit_ads/<int:id>")
def edit_single_ad(id):
    item_owner = get_item_owner(id) 
    if item_owner != get_user_id():
        return render_template("error.html", message="Et voi muokata tätä tuotetta, sillä et omista sitä!")
    item = get_single_item((id))
    return render_template("edit_single_ad.html", item=item)

@app.route("/update_ad", methods=["POST"])
def update_ad():
    if session["csrf_token"] != request.form["csrf_token"]: 
        return False

    id = request.form["id"]
    name = request.form["name"]
    hinta = request.form["hinta"]
    kuvaus = request.form["kuvaus"]
    picture = request.files["picture"]

    item_owner = get_item_owner(id) 
    if item_owner != get_user_id():
        return render_template("error.html", message="Et voi muokata tätä tuotetta, sillä et omista sitä!")

    try:
        hinta = parse_price(hinta)
    except:
        return render_template("error.html", message="Hinnan täytyy olla numero")

    if len(name) > 50 or len(kuvaus) > 150 or hinta > 1000000000:
        return render_template("error.html", message="Liian pitkä rimpsu informaatiota!")

    if picture:
        update_ad_with_picture(name, hinta, kuvaus, picture, id)
    else:
        update_ad_without_picture(name, hinta, kuvaus, id)
    return redirect("/edit_ads")

@app.route("/delete_ad/<int:id>")
def delete_ad(id):
    item_owner = get_item_owner(id)
    if item_owner != get_user_id():
        return render_template("error.html", message="Et voi poistaa tätä tuotetta, sillä et omista sitä!")
    delete_item_by_id(id)
    return redirect("/edit_ads")