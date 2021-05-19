from db import db

def get_admin_password(username):
    sql = "SELECT password FROM admin WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    admin = result.fetchone()
    return admin

def insert_new_category(new):
    sql = "INSERT INTO categories (name) VALUES (:new)"
    db.session.execute(sql, {"new":new})
    db.session.commit()