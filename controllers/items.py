from db_operations.items_db import *
from flask import render_template, request, redirect
from app import app

# Individual category page
@app.route("/category/<int:id>/<int:page>/<sort>")
def category(id,page,sort):
    category = get_category_name(id)

    if sort == 'new':
        items = get_offsetted_newest_items_by_category_id(id, page)
    else:
        items = get_offsetted_oldest_items_by_category_id(id, page)
    
    return render_template("category.html", category=category, items=items, id=id, page=page, sort=sort)

# Individual items page
@app.route("/item/<int:id>")
def item(id):
    try:
        item = get_item_by_id(id)
    except IndexError:
        return render_template("error.html", message="Tuotetta ei löydy")
    item_name = item[2]
    date_added = item[3]
    user_id = item[5]
    price = item[6]
    kuvaus = item[7]
    picture = item[8]
    

    seller_name = get_seller_name(user_id)
    seller_result = get_other_seller_info(user_id)

    seller_number = seller_result[0] 
    seller_location = seller_result[1] 
    seller_email = seller_result[2] 
    seller_description = seller_result[3] 

    return render_template("item.html", item_name=item_name, date_added=date_added, 
                            price=price, kuvaus=kuvaus, picture=picture,
                            seller_name=seller_name, seller_description=seller_description,puhnro=seller_number,
                            pkunta=seller_location, seller_email=seller_email)

# Search page results
@app.route("/search", methods=["POST"])
def search():
    search = "%"+request.form["search"]+"%"
    if len(search) > 50: 
        return render_template("error.html", message="Liian pitkä hakusana")

    items = get_items_by_search_parameters(search)

    return render_template("search_results.html", search=search[1:-1], items=items)