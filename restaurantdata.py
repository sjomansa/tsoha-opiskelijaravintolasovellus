#Functionality for fetching and editing restaurant-data
from db import db
from sqlalchemy.sql import text
from comments import get_messages
import secrets



def get_main_restaurantdata(name=None):

    if name:
        
        sql = text("""SELECT R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS stars, COALESCE(ROUND(AVG(r_quetimes.que_time), 0),0) AS wait_time,
        R.city AS city FROM users U JOIN restaurants R ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
        WHERE U.username =:name GROUP BY R.name, U.username, R.city;""")

        result = db.session.execute(sql, {"name":name})

        restaurants_data = result.fetchall()
    
    else:

        sql = text("""SELECT R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS stars, COALESCE(ROUND(AVG(r_quetimes.que_time), 0),1) AS wait_time,
        R.city AS city FROM users U JOIN restaurants R ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
        GROUP BY R.name, U.username, R.city;""")

        result = db.session.execute(sql)

        restaurants_data = result.fetchall()

    return restaurants_data


def get_singular_restaurantdata(name: str):

    sql = text("""
            SELECT R.id AS id, R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_quetimes.que_time), 1),1) AS wait_time, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS rating,
            R.city AS city, R.address AS address FROM restaurants R JOIN users U ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
            WHERE R.name =:name GROUP BY R.id, R.name, U.username, R.city, R.address;
            """)
    result = db.session.execute(sql, {"name":name})
    restaurant = result.fetchone()

    if restaurant is None:
        return None

    sql = text("""
            SELECT r_i.infotext AS infotext, r_i.open_times AS open_times FROM restaurants LEFT JOIN r_info r_i ON r_i.r_id = restaurants.id 
            WHERE restaurants.name =:name;
            """)
    result = db.session.execute(sql, {"name":name})
    info = result.fetchone()

    sql = text("""
        SELECT M.food AS food, M.price AS price FROM restaurants R LEFT JOIN r_menus AS M ON R.id = M.r_id 
        WHERE R.name =:name;
        """)
    result = db.session.execute(sql, {"name":name})
    menu = result.fetchall()

    messages = get_messages(restaurant.id)

    return restaurant, info, menu, messages


def create_new_restaurant(owner_id, name, address, city):

    sql = text("""
               INSERT INTO restaurants (owner_id, name, address, city) VALUES (:owner_id, :name, :address, :city)
               """)
    try:
        db.session.execute(sql, {"owner_id":owner_id, "name":name, "address":address, "city":city})
        db.session.commit()
        print("success")
    except Exception as e:
        raise ValueError("Error creating a new restaurant")
        