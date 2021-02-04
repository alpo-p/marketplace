from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from db import db
from app import app 

from datetime import datetime

import psycopg2

@app.route("/")
def index():
    return render_template("index.html")

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
    print(items)
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
