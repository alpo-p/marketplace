from flask import render_template, request, redirect
from db import db
from app import app

# Individual category page
@app.route("/category/<int:id>/<int:page>/<sort>")
def category(id,page,sort):
    sql = "SELECT name FROM categories WHERE id=:cid"
    result = db.session.execute(sql, {"cid":id})
    category = result.fetchall()[0][0]

    if sort == 'new':
        sql = "SELECT * FROM items WHERE category_id=:id ORDER BY date_added DESC " \
          "LIMIT 5 OFFSET :offset"
    else:
        sql = "SELECT * FROM items WHERE category_id=:id ORDER BY date_added ASC " \
          "LIMIT 5 OFFSET :offset"
    result = db.session.execute(sql, {"id":id, "offset":(page-1)*5})
    items = result.fetchall()
    return render_template("category.html", category=category, items=items, id=id, page=page, sort=sort)

# Individual items page
@app.route("/item/<int:id>")
def item(id):
    sql = "SELECT * FROM items WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    try:
        item = result.fetchall()[0]
    except IndexError:
        return render_template("error.html", message="Tuotetta ei löydy")
    item_name = item[2]
    date_added = item[3]
    visible = item[4]
    if not visible:
        return render_template("error.html", message="Tuotetta ei enää löydy")
    user_id = item[5]
    price = item[6]
    kuvaus = item[7]
    picture = item[8]
    

    sql = "SELECT username FROM users WHERE id=:user_id"
    seller_name = db.session.execute(sql, {"user_id":user_id}).fetchone()[0]
    sql = "SELECT puhelinnumero, paikkakunta, sposti, kuvaus FROM userinfo WHERE user_id=:user_id"
    seller_result = db.session.execute(sql,{"user_id":user_id}).fetchall()[0]
    seller_number = seller_result[0] 
    seller_location = seller_result[1] 
    seller_email = seller_result[2] 
    seller_description = seller_result[3] 

    return render_template("item.html", item_name=item_name, date_added=date_added, 
                            price=price, kuvaus=kuvaus, picture=picture,
                            seller_name=seller_name, seller_description=seller_description,puhnro=seller_number,
                            pkunta=seller_location, seller_email=seller_email)

@app.route("/search", methods=["POST"])
def search():
    search = "%"+request.form["search"]+"%"
    sql = "SELECT * FROM items WHERE name ILIKE :search LIMIT 15"
    result = db.session.execute(sql, {"search":search})
    items = result.fetchall()
    return render_template("search_results.html", search=search[1:-1], items=items)