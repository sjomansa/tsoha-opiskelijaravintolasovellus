from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
import secrets



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

#Get current session user_id
def get_username():
    return session["user"] if session["user"] else 0

#Get messages for a given restaurant
def get_messages(restaurant_id):
    sql = text("""
            SELECT U.username as name, M.message AS message, M.time AS time FROM messages M JOIN users U ON M.u_id = U.id 
            WHERE M.r_id =:restaurant_id ORDER BY M.time DESC;
            """)
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    messages = result.fetchall()
    return messages

#Check if user is signed, otherwise redirect to login page
@app.before_request
def check_login():
    if request.endpoint not in ['index', 'register', 'login']:
        if not session.get('user'):
            return redirect("/")


#Display index view
@app.route("/")
def index():
    return render_template("index.html")

#Display view for registering a new user
@app.route("/register")
def register():
    return render_template("register.html")


#Check if login is valid and set session-objects information
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
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
            return redirect("/restaurants")
        
    return redirect("/register")


#Main restaurant view of opiskelijaravintolat, where you can see the list of all restaurants
@app.route("/restaurants")
def restaurants_view():

    sql = text("""SELECT R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS stars, COALESCE(ROUND(AVG(r_quetimes.que_time), 0),1) AS wait_time,
    R.city AS city FROM users U JOIN restaurants R ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
    GROUP BY R.name, U.username, R.city;""")

    result = db.session.execute(sql)

    restaurants_data = result.fetchall()

    return render_template("restaurants.html", restaurants=restaurants_data)


@app.route("/restaurants/<name>")
def restaurant_info(name):

    sql = text("""
            SELECT R.id AS id, R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_quetimes.que_time), 1),1) AS wait_time, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS rating,
            R.city AS city, R.address AS address FROM restaurants R JOIN users U ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
            WHERE R.name =:name GROUP BY R.id, R.name, U.username, R.city, R.address;
            """)
    result = db.session.execute(sql, {"name":name})
    restaurant = result.fetchone()

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

    return render_template("restaurantlayout.html", restaurant=restaurant, info=info, menu=menu, messages=messages)


#Function for sending a message to restaurants message board
@app.route("/send_message", methods = ["POST"])
def send_message():
    user_id = session["user_id"]
    restaurant_id = request.form["restaurant_id"]
    restaurant_name = request.form["restaurant_name"]
    message = request.form["content"]
    
    #Check if message is too long
    if len(message) > 500:
        return redirect("/") #Add error message here
    
    #Check that the session token matches users:
    if session["csrf_token"] != request.form["csrf_token"]:
        return redirect("/") #Add error message here
    
    sql = text("INSERT INTO messages (r_id, u_id, message, time) VALUES (:r_id, :u_id, :message, NOW())")
    db.session.execute(sql, {"r_id":restaurant_id, "u_id":user_id, "message":message})
    db.session.commit()

    return redirect(f"/restaurants/{restaurant_name}")


#Function for registering a new user from register.html
@app.route("/register_user", methods=["POST"])
def register_user():
    password = request.form["password1"]
    username = request.form["username"]

    #Look up if its a student or a restaurant
    status = request.form["admin"]

    admin = False
    if status == "ravintoloitsija":
        admin = True

    #Look up if the user is already in the database
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if password == request.form["password2"] and len(password) > 4:
        if not user:
            sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
            hash_value = generate_password_hash(password)
            db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
            db.session.commit()
            return redirect("/")
      
    return redirect("/register")


