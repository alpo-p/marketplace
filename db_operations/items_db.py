from db import db

def get_newest():
    sql = "SELECT * FROM items ORDER BY date_added DESC LIMIT 3"
    result = db.session.execute(sql)
    items = result.fetchall()
    return items

def get_offsetted_oldest_items_by_category_id(id, page):
    sql = "SELECT * FROM items WHERE category_id=:id ORDER BY date_added ASC " \
          "LIMIT 5 OFFSET :offset"
    result = db.session.execute(sql, {"id":id, "offset":(page-1)*5})
    return result.fetchall()

def get_offsetted_newest_items_by_category_id(id, page):
    sql = "SELECT * FROM items WHERE category_id=:id ORDER BY date_added DESC " \
          "LIMIT 5 OFFSET :offset"
    result = db.session.execute(sql, {"id":id, "offset":(page-1)*5})
    return result.fetchall()

def get_category_name(id):
    sql = "SELECT name FROM categories WHERE id=:cid"
    result = db.session.execute(sql, {"cid":id})
    return result.fetchall()[0][0]

def get_other_seller_info(user_id):
    sql = "SELECT puhelinnumero, paikkakunta, sposti, kuvaus FROM userinfo WHERE user_id=:user_id"
    seller_result = db.session.execute(sql,{"user_id":user_id}).fetchall()[0]
    return seller_result

def get_seller_name(user_id):
    sql = "SELECT username FROM users WHERE id=:user_id"
    seller_name = db.session.execute(sql, {"user_id":user_id}).fetchone()[0]
    return seller_name

def get_item_by_id(id):
    sql = "SELECT * FROM items WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()[0]

def get_items_by_search_parameters(search):
    sql = "SELECT * FROM items WHERE name ILIKE :search LIMIT 15"
    result = db.session.execute(sql, {"search":search})
    return result.fetchall()