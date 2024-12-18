#Functionality for commenting
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


#Fetch messages from specific restaurant
def get_messages(restaurant_id):
    sql = text("""
            SELECT U.username as name, M.message AS message, M.time AS time FROM messages M JOIN users U ON M.u_id = U.id 
            WHERE M.r_id =:restaurant_id ORDER BY M.time DESC;
            """)
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    messages = result.fetchall()
    return messages

#insert comment into the database from a specific restaurant
def insert_comment(user_id, restaurant_id, restaurant_name, message, token, session):

    if len(message) > 500:
        raise ValueError("Viestin enimmäispituus on 500 merkkiä. Syötä lyhyempi viesti.")
    
    if message == "":
        raise ValueError("Viestissä pitää lukea jotain. Syötä vähintään yksi kirjain.")

    #Check that the session token matches users:
    if session["csrf_token"] != token:
        raise ValueError("Senders CRSF-token does not match the session token.") 
    
    sql = text("INSERT INTO messages (r_id, u_id, message, time) VALUES (:r_id, :u_id, :message, NOW())")

    try:
        db.session.execute(sql, {"r_id":restaurant_id, "u_id":user_id, "message":message})
        db.session.commit()
    except:
        raise ValueError("VIrhe viestin lisäämisessä serverille.")

    return True