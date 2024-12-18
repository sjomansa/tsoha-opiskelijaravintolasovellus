from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

#Methods for handling and updating user-specific information.


#Checks the password and username. Assigns the session data if login is succesful.
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
            raise ValueError("Väärä salasana, yritä uudelleen")
        
    else:
        raise ValueError("Käyttäjänimeä ei löytynyt, kirjoititko sen oikein?")

#For logging out. Deletes the session data.  
def logout_user(session):
    del session["user"]
    del session["user_id"]
    del session["admin"]
    del session["csrf_token"]

#For registering a new user. Checks if the passwords match and inserts the information into the database if succesful.
def register_user(username, password1, password2, admin):

    if password1 != password2:
        raise ValueError("Salasanat eivät täsmää, oletko varma, että ne ovat oikein?")
    
    if not len(password1) > 4:
        raise ValueError("Salasanan pitää olla vähintään 5 merkkiä pitkä. Syötä uusi salasana")
    
    if not username:
        raise ValueError("Käyttäjätunnuksen pitää olla ainakin yksi merkki")

    #Look up if the user is already in the database
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user:
        raise ValueError("Käyttäjätunnus jo käytössä, valitse joku toinen")

    try:
        sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
        hash_value = generate_password_hash(password1)
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
    except:
        raise ValueError("Error registering a new user")
      
    return True