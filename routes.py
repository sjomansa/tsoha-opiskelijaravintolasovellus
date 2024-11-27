#Application routes and their functions
from app import app
from flask import redirect, render_template, request, session
from users import login_user, logout_user, register_user
from restaurantdata import get_main_restaurantdata, get_singular_restaurantdata, create_new_restaurant
from comments import insert_comment

@app.route("/")
def index():
    if session.get("user"):
        return redirect("/restaurants")
    else:
        return render_template("login.html")


#Display view for registering a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        username = request.form["username"]

        #Look up if its a student or a restaurant
        status = request.form["admin"]

        admin = False
        
        if status == "ravintoloitsija":
            admin = True

        try:
            register_user(username, password1, password2, admin)
        except Exception as e:
            return render_template("error.html", message=e)
        
        return redirect("/")


#Check if login is valid and set session-objects information
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    try:
        login_user(username, password, session)
        
        return redirect("/restaurants")
    
    except:
        return render_template("error.html", message="Kirjautuminen epäonnistui") #Add more detailed error message here
    

@app.route("/logout")
def logout():

    logout_user(session)
    return redirect("/")


    # sql = text("SELECT password, admin, id FROM users WHERE username=:username")
    # result = db.session.execute(sql, {"username": username})
    # user = result.fetchone()

    # if user:
    #     hash_value = user.password
    #     if check_password_hash(hash_value, password):
    #         session["user"] = username
    #         session["user_id"] = user.id
    #         session["admin"] = user.admin
    #         session["csrf_token"] = secrets.token_hex(16)
    #         return redirect("/restaurants")
        
    # return redirect("/register")


#Main restaurant view of opiskelijaravintolat, where you can see the list of all restaurants
@app.route("/restaurants")
def restaurants_view():

    # sql = text("""SELECT R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS stars, COALESCE(ROUND(AVG(r_quetimes.que_time), 0),1) AS wait_time,
    # R.city AS city FROM users U JOIN restaurants R ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
    # GROUP BY R.name, U.username, R.city;""")

    # result = db.session.execute(sql)

    # restaurants_data = result.fetchall()

    restaurants_data = get_main_restaurantdata()

    return render_template("restaurants.html", restaurants=restaurants_data)


@app.route("/restaurants/<name>")
def restaurant_info(name):

    # sql = text("""
    #         SELECT R.id AS id, R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_quetimes.que_time), 1),1) AS wait_time, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS rating,
    #         R.city AS city, R.address AS address FROM restaurants R JOIN users U ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
    #         WHERE R.name =:name GROUP BY R.id, R.name, U.username, R.city, R.address;
    #         """)
    # result = db.session.execute(sql, {"name":name})
    # restaurant = result.fetchone()

    # sql = text("""
    #         SELECT r_i.infotext AS infotext, r_i.open_times AS open_times FROM restaurants LEFT JOIN r_info r_i ON r_i.r_id = restaurants.id 
    #         WHERE restaurants.name =:name;
    #         """)
    # result = db.session.execute(sql, {"name":name})
    # info = result.fetchone()

    # sql = text("""
    #     SELECT M.food AS food, M.price AS price FROM restaurants R LEFT JOIN r_menus AS M ON R.id = M.r_id 
    #     WHERE R.name =:name;
    #     """)
    # result = db.session.execute(sql, {"name":name})
    # menu = result.fetchall()

    # messages = get_messages(restaurant.id)

    restaurant, info, menu, messages = get_singular_restaurantdata(name)

    if restaurant is None:
        return render_template("error.html", message = "No restaurant found, are you sure this restaurant exists?")

    return render_template("restaurantlayout.html", restaurant=restaurant, info=info, menu=menu, messages=messages)


@app.route("/<user>/restaurants")
def admin_restaurants_view(user):

    if session["admin"]:

        restaurant_data = get_main_restaurantdata(name=user)

        return render_template("restaurants_admin_view.html", restaurants = restaurant_data )
    
    else:

        return render_template("error.html", message="Sinulla ei ole oikeuksia päästä tälle sivulle :(")
    
@app.route("/<user>/restaurants/<restaurant_name>")
def admin_restaurant_view(user, restaurant_name):

    if session["admin"]:

        restaurant_data = get_singular_restaurantdata(name=restaurant_name)

        if restaurant_data[0].owner != session["user"]:
            return render_template("error.html", message="Sinulla ei ole oikeuksia päästä tälle sivulle :(")

        return render_template("restaurant_admin_view.html")
    else:

        return render_template("error.html", message="Sinulla ei ole oikeuksia päästä tälle sivulle :(")

#Function for sending a message to restaurants message board
@app.route("/send_message", methods = ["POST"])
def send_message():

    user_id = session["user_id"]
    restaurant_id = request.form["restaurant_id"]
    restaurant_name = request.form["restaurant_name"]
    message = request.form["content"]
    crsf_token = request.form["csrf_token"]

    # #Check if message is too long
    # if len(message) > 500:
    #     return redirect("/restaurants/{restaurant_name}") #Add error message here

    try:
        insert_comment(user_id, restaurant_id, restaurant_name, message, crsf_token, session)
    except Exception as e:
        return render_template("error.html", message = e)
    
    # #Check that the session token matches users:
    # if session["csrf_token"] != request.form["csrf_token"]:
    #     return redirect("/") #Add error message here
    
    # sql = text("INSERT INTO messages (r_id, u_id, message, time) VALUES (:r_id, :u_id, :message, NOW())")
    # db.session.execute(sql, {"r_id":restaurant_id, "u_id":user_id, "message":message})
    # db.session.commit()

    return redirect(f"/restaurants/{restaurant_name}")

@app.route("/<user>/restaurants/new_restaurant", methods = ["GET", "POST"])
def create_restaurant(user):

    if request.method == "GET":
        return render_template("create_restaurant_view.html", user=user)
    else:
        try:
            user_id = session["user_id"]
            name = request.form["name"]
            address = request.form["address"]
            city = request.form["city"]
            create_new_restaurant(user_id, name, address, city)
            return redirect("/{session.user}/restaurants")
        except Exception as e:
            return render_template("error.html", message=e)



# @app.route("/register_user", methods=["POST"])
# def register_user():
#     password = request.form["password1"]
#     username = request.form["username"]

#     #Look up if its a student or a restaurant
#     status = request.form["admin"]

#     admin = False
#     if status == "ravintoloitsija":
#         admin = True

#     #Look up if the user is already in the database
#     sql = text("SELECT id FROM users WHERE username=:username")
#     result = db.session.execute(sql, {"username": username})
#     user = result.fetchone()
#     if password == request.form["password2"] and len(password) > 0:
#         if not user:
#             sql = text("INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)")
#             hash_value = generate_password_hash(password)
#             db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
#             db.session.commit()
#             print(f"Sucess for {username} with password {hash_value}, status {admin}")
#             return redirect("/")
      
#     return redirect("/register")