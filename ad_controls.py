from boto3 import resource
from flask import render_template, redirect, request, session
from db import db
from app import app
from file_management import upload_picture

def get_user_id():
    sql = "SELECT id FROM users WHERE username=:name"
    name = session["username"]
    user_id = db.session.execute(sql, {"name":name}).fetchone()[0]
    return user_id

@app.route("/add_ad")
def add_ad():
    return render_template("add_ad.html")

@app.route("/upload_ad", methods=["POST"])
def make_ad():
    name = request.form["name"]
    category = request.form["category"]
    kuvaus = request.form["kuvaus"]
    hinta = int(request.form["hinta"].replace(" ","").replace("e","").replace("€","").replace("E",""))

    picture = request.files['picture']
    pic_name = upload_picture(picture)

    user_id = get_user_id()

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
    sql = "SELECT * FROM items WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    items = result.fetchall()
    return render_template("edit_ads.html", items=items)

@app.route("/edit_ads/<int:id>")
def edit_single_ad(id):
    sql = "SELECT * FROM items WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    item = result.fetchone()
    return render_template("edit_single_ad.html", item=item)

@app.route("/update_ad", methods=["POST"])
def update_ad():
    id = request.form["id"]
    name = request.form["name"]
    price = request.form["hinta"]
    kuvaus = request.form["kuvaus"]
    picture = request.files["picture"]
    if picture:
        pic_name = upload_picture(picture)
        sql = "UPDATE items SET name=:name, price=:price, kuvaus=:kuvaus, picture=:picture " \
              "WHERE id=:id"
        db.session.execute(sql, {"name":name,"price":price,"kuvaus":kuvaus,"picture":pic_name,"id":id})
    else:
        sql = "UPDATE items SET name=:name, price=:price, kuvaus=:kuvaus " \
              "WHERE id=:id"
        db.session.execute(sql, {"name":name,"price":price,"kuvaus":kuvaus,"id":id})
    db.session.commit()
    return redirect("/edit_ads")

@app.route("/delete_ad/<int:id>")
def delete_ad(id):
    sql = "DELETE FROM items WHERE id=:id"
    db.session.execute(sql,{"id":id})
    db.session.commit()
    return redirect("/edit_ads")
