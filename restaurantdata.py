#Functionality for fetching and editing restaurant-data
from db import db
from sqlalchemy.sql import text
from comments import get_messages
import secrets


#Get the data for the main view of all restaurants. Includes sorting-order functionality.
def get_main_restaurantdata(name=None, sort=None, sortorder=None):

    if name:
        
        sql = text("""SELECT R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS stars, COALESCE(ROUND(AVG(r_quetimes.que_time), 0),0) AS wait_time,
        R.city AS city FROM users U JOIN restaurants R ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
        WHERE U.username =:name GROUP BY R.name, U.username, R.city;""")

        result = db.session.execute(sql, {"name":name})

        restaurants_data = result.fetchall()
    
    else:
        #Check if any ordering of data is required
        if not sort:

            sql = text("""SELECT R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS stars, COALESCE(ROUND(AVG(r_quetimes.que_time), 0),1) AS wait_time,
            R.city AS city FROM users U JOIN restaurants R ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
            GROUP BY R.name, U.username, R.city;""")

            result = db.session.execute(sql)

            restaurants_data = result.fetchall()
        
        else:

            if sort == "Ravintola":
                sortvalue = "name"
            elif sort == "Ravintoloitsija":
                sortvalue = "owner"
            elif sort == "tahdet":
                sortvalue = "stars"
            elif sort == "odotusaika":
                sortvalue = "wait_time"
            else:
                sortvalue = "city"
            
            sql = f"""SELECT R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS stars, COALESCE(ROUND(AVG(r_quetimes.que_time), 0),1) AS wait_time,
            R.city AS city FROM users U JOIN restaurants R ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
            GROUP BY R.name, U.username, R.city ORDER BY {sortvalue} {sortorder}"""

            result = db.session.execute(text(sql))

            restaurants_data = result.fetchall()


    return restaurants_data

#Get data for a single restaurant from the database.
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
        SELECT M.id AS id, M.food AS food, M.price AS price FROM restaurants R LEFT JOIN r_menus AS M ON R.id = M.r_id 
        WHERE R.name =:name;
        """)
    result = db.session.execute(sql, {"name":name})
    menu = result.fetchall()

    messages = get_messages(restaurant.id)

    return restaurant, info, menu, messages

#Insert a new restaurant into the database.
def create_new_restaurant(owner_id, name, address, city, token, session):

    if name == "":
        raise ValueError("Syötä kelvollinen nimi, nimen pitää olla ainakin yhden merkin pituinen")
    
    if address == "":
        raise ValueError("Syötä kelvollinen osoite, osoitteen pitää olla ainakin yhden merkin pituinen")
    
    if city == "":
        raise ValueError("Syötä kelvollinen kaupunki, kaupungin nimen pitää olla ainakin yhden merkin pituinen")


    #Check if username is taken
    if get_singular_restaurantdata(name) == None:

        if session["csrf_token"] != token:
            raise ValueError("Error creating restaurant, you csrf-token does not match the users")
        

        sql = text("""
            INSERT INTO restaurants (owner_id, name, address, city) VALUES (:owner_id, :name, :address, :city)
            """)
        try:
            db.session.execute(sql, {"owner_id":owner_id, "name":name, "address":address, "city":city})
            db.session.commit()
            #print("success")
        except Exception as e:
            raise ValueError("Error creating a new restaurant")
    #Else block if username is taken
    else:
        raise ValueError("Ravintolaa ei voitu luoda, nimi on jo käytössä")

    

    
#Update the menu in the database according to the menuitems id. 
def update_menu(item_id, food, price):

    sql = text('''
        UPDATE r_menus
        SET food =:food, price =:price
        WHERE id =:item_id
    '''
    )
    try:

        db.session.execute(sql, {"food":food, "price":price, "item_id":item_id})
        db.session.commit()
    except Exception as e:
        raise ValueError("Error updating the menu :/")

#Update the information for a specific restaurant.
def update_restaurant_info(r_id, name, address, city, info, open_times):

    sql = text('''
        UPDATE restaurants
        SET name =:name, address =:address, city =:city
        WHERE id =:r_id
    '''
    )

    #Check that the input is not empty

    if name == "":
        raise ValueError("Ravintolalla pitää olla nimi, syötä vähintään yksi kirjain")
    
    if address == "":
        raise ValueError("Ravintolalla pitää olla kelvollinen osoite. Se ei voi olla tyhjä.")
    
    if city == "":
        raise ValueError("Ravintolalla pitää olla kelvollinen kaupunki. Se ei voi olla tyhjä.")
    
    if info == "":
        raise ValueError("Infoteksti-kenttä ei voi olla tyhjä.")
    
    if open_times == "":
        raise ValueError("Aukioloaika-kenttä ei voi olla tyhjä.")

    try:
        db.session.execute(sql, {"name":name, "address":address, "city":city, "r_id":r_id})
        db.session.commit()
    except Exception as e:
        raise ValueError("Error updating the restaurants name and address information :/")
    
    #Check if there is a current infotext of the restaurant. If not, create one.
    
    sql = text("SELECT infotext FROM r_info WHERE r_id =:r_id")

    result = db.session.execute(sql, {"r_id":r_id})
    current_info = result.fetchone()

    if not current_info:
        sql = text('''
                   INSERT INTO r_info (r_id, infotext, open_times)
                   VALUES (:r_id, :infotext, :open_times)
                   ''')
        try:
            db.session.execute(sql, {"r_id":r_id, "infotext":info, "open_times":open_times})
            db.session.commit()
        except:
            raise ValueError("Error creating an infotext to the restaurant")

    #If info exists, we only need to update the database
    else:
        sql = text('''
            UPDATE r_info
            SET infotext =:infotext, open_times =:open_times
            WHERE r_id =:r_id
        '''
        )

        try:
            db.session.execute(sql, {"infotext":info, "open_times":open_times, "r_id":r_id})
            db.session.commit()
        except:
            raise ValueError("Error updating the information-text and opening-times")

#Insert a new menuitem to the database.   
def insert_menuitem(r_id, food, price):

    r_id = int(r_id)
    try:
        sql = text('''
            INSERT INTO r_menus (r_id, food, price) VALUES (:r_id, :food, :price)
        '''
           )
        db.session.execute(sql, {"r_id":r_id, "food":food, "price":price})
        db.session.commit()
    except:
        raise ValueError("Error inserting a new menuitem")

#Delete an item from the database. 
def delete_menuitem(id):

    sql = text("DELETE FROM r_menus WHERE id =:id")

    try:
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        raise ValueError("Could not delete item")
    
#Insert a rating to the database according to the restaurants id.
def insert_rating(id, rating):

    try:
        sql = text("INSERT INTO r_stars (r_id, rating) VALUES (:r_id, :rating)")
        db.session.execute(sql, {"r_id":id, "rating":rating})
        db.session.commit()
    except Exception as e:
        raise ValueError(e)

#Insert a quetime to the database according to the restaurants id.
def insert_quetime(id, quetime):

    try:
        sql = text("INSERT INTO r_quetimes (r_id, que_time) VALUES (:r_id, :que_time)")
        db.session.execute(sql, {"r_id":id, "que_time":quetime})
        db.session.commit()
    except:
        raise ValueError("Error inserting quetime to server")

#Delete a restaurant from the database.

def delete_restaurant_from_db(r_id, token, session):
    if token != session["csrf_token"]:
        raise ValueError("Error deleting restaurant: Your CSRF-token does not match owners!")
    try:
        sql = text("DELETE FROM restaurants WHERE id =:r_id")
        db.session.execute(sql, {"r_id":r_id})
        db.session.commit()
    except Exception as e:
        raise ValueError(f"Error deleting restaurant {e}")