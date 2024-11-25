#Functionality for commenting
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash



def get_messages(restaurant_id):
    sql = text("""
            SELECT U.username as name, M.message AS message, M.time AS time FROM messages M JOIN users U ON M.u_id = U.id 
            WHERE M.r_id =:restaurant_id ORDER BY M.time DESC;
            """)
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    messages = result.fetchall()
    return messages


def insert_comment(user_id, restaurant_id, restaurant_name, message, token, session):

    if len(message) > 500:
        raise ValueError("Input exceeded the maximum limit of 500 characters.")

    #Check that the session token matches users:
    if session["csrf_token"] != token:
        raise ValueError("Senders CRSF-token does not match the session token.") 
    
    sql = text("INSERT INTO messages (r_id, u_id, message, time) VALUES (:r_id, :u_id, :message, NOW())")

    try:
        db.session.execute(sql, {"r_id":restaurant_id, "u_id":user_id, "message":message})
        db.session.commit()
    except:
        raise ValueError("Error inserting comment into the database.")

    return True