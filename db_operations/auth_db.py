from flask import session
from db import db

def get_user_id():
    sql = "SELECT id FROM users WHERE username=:name"
    try:
        name = session["username"]
    except:
        return False
    user_id = db.session.execute(sql, {"name":name}).fetchone()[0]
    return user_id

def get_user_password(username):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql,{"username":username})
    user = result.fetchone()
    return user

def get_all_usernames():
    return db.session.execute("SELECT username FROM users").fetchall()

def insert_user_info_to_db(sposti, puhelinnumero, paikkakunta, kuvaus, user_id):
    sql_b = "INSERT INTO userinfo (user_id,puhelinnumero,paikkakunta,sposti, kuvaus)" \
            "VALUES (:user_id,:puhelinnumero,:paikkakunta,:sposti,:kuvaus)"
    db.session.execute(sql_b, 
        {"user_id":user_id,"puhelinnumero":puhelinnumero,"paikkakunta":paikkakunta,"sposti":sposti,"kuvaus":kuvaus})
    db.session.commit()

def create_auth_user(username, hashed_pwd):
    sql_a = "INSERT INTO users (username,password)" \
            "VALUES (:username,:password) RETURNING id"
    result_a = db.session.execute(sql_a, {"username":username,"password":hashed_pwd})
    db.session.commit()
    user_id = result_a.fetchone()[0]
    return user_id

def get_all_emails():
    return db.session.execute("SELECT sposti FROM userinfo").fetchall()
