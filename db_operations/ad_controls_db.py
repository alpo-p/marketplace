from db import db
from file_management import upload_picture

def commit_new_ad_to_DB_and_return_item_id(category, name, user_id, hinta, kuvaus, pic_name):
    sql_a = "INSERT INTO items (category_id, name, date_added, visible, user_id, price, kuvaus, picture)" \
                "VALUES (:category, :name, NOW(), TRUE, :user_id, :price, :kuvaus, :picture) RETURNING id"
    result_a = db.session.execute(sql_a, {"category":category,"name":name, "user_id":user_id, "price":hinta, "kuvaus":kuvaus,
                                          "picture":pic_name})
    db.session.commit()
    return result_a.fetchone()[0]

def get_all_items_by_user_id(user_id):
    sql = "SELECT * FROM items WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_item_owner(id):
    return db.session.execute("SELECT user_id from items WHERE id=:id", {"id":id}).fetchone()[0]

def get_single_item(id):
    sql = "SELECT * FROM items WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def update_ad_with_picture(name, hinta, kuvaus, picture, id):
    pic_name = upload_picture(picture)
    sql = "UPDATE items SET name=:name, price=:price, kuvaus=:kuvaus, picture=:picture " \
            "WHERE id=:id"
    db.session.execute(sql, {"name":name,"price":hinta,"kuvaus":kuvaus,"picture":pic_name,"id":id})
    db.session.commit()

def update_ad_without_picture(name, hinta, kuvaus, id):
    sql = "UPDATE items SET name=:name, price=:price, kuvaus=:kuvaus " \
            "WHERE id=:id"
    db.session.execute(sql, {"name":name,"price":hinta,"kuvaus":kuvaus,"id":id})
    db.session.commit()

def delete_item_by_id(id):
    sql = "DELETE FROM items WHERE id=:id"
    db.session.execute(sql,{"id":id})
    db.session.commit()