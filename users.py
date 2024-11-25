from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets




def login_user(username, password, session):
    
    sql = text("SELECT password, admin, id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user"] = username
            session["user_id"] = user.id
            session["admin"] = user.admin
            session["csrf_token"] = secrets.token_hex(16)
            
            return True
        else:
            raise ValueError("Incorrect password")
        
    else:
        raise ValueError("Username not found, are you already registered?")

def register_user(username, password1, password2, admin):

    if password1 != password2:
        raise ValueError("Entered passwords don't match")
    
    if not len(password1) > 4:
        raise ValueError("Password needs to be at least 5 characters")
    
    if not username:
        raise ValueError("Username needs to be at least one character long")

    #Look up if the user is already in the database
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        raise ValueError("Username already in use, please select another one")

    try:
        sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
        hash_value = generate_password_hash(password1)
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
    except:
        raise ValueError("Error registering a new user")
      
    return True