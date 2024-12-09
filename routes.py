#Application routes and their functions
from app import app
from flask import redirect, render_template, request, session
from users import login_user, logout_user, register_user
from restaurantdata import get_main_restaurantdata, get_singular_restaurantdata, create_new_restaurant, update_menu, update_restaurant_info, insert_menuitem, delete_menuitem, insert_rating, insert_quetime, delete_restaurant_from_db
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
@app.route("/restaurants", methods=["GET", "POST"] )
def restaurants_view():

    # sql = text("""SELECT R.name AS name, U.username AS owner, COALESCE(ROUND(AVG(r_stars.rating), 1), 0) AS stars, COALESCE(ROUND(AVG(r_quetimes.que_time), 0),1) AS wait_time,
    # R.city AS city FROM users U JOIN restaurants R ON U.id = R.owner_id LEFT JOIN r_stars ON r_stars.r_id = R.id LEFT JOIN r_quetimes ON r_quetimes.r_id = R.id
    # GROUP BY R.name, U.username, R.city;""")

    # result = db.session.execute(sql)

    # restaurants_data = result.fetchall()
    if request.method == "GET":

        restaurants_data = get_main_restaurantdata()

    else:

        sortvalue = request.form["sortvalue"]
        sortorder = request.form["sortorder"]

        if sortvalue == "1":
            restaurants_data = get_main_restaurantdata()

        else:
            restaurants_data = get_main_restaurantdata(sort = sortvalue, sortorder= sortorder)

    return render_template("restaurants.html", restaurants=restaurants_data)


@app.route("/restaurants/<name>", methods=["GET", "POST"])
def restaurant_info(name):

    restaurant, info, menu, messages = get_singular_restaurantdata(name)

    if restaurant is None:
            return render_template("error.html", message = "No restaurant found, are you sure this restaurant exists?")

    if request.method == "GET":

        return render_template("restaurantlayout.html", restaurant=restaurant, info=info, menu=menu, messages=messages)
    
    else:

        try:
            r_id = restaurant.id
            quetime = int(request.form["quetime"])
            insert_quetime(r_id, quetime)
            return redirect(f"/restaurants/{name}")
        
        except:  
            return render_template("error.html", message="Ongelma odotusajan lisäämisessä palvelimelle")



@app.route("/restaurants/<name>/rate_restaurant", methods = ["GET", "POST"])
def rate_restaurant(name):
    if request.method == "GET":
        return render_template("add_rating_view.html", name=name)
    
    else:
        #Add rating to the database and go back to restaurant-view
        rating = int(request.form["rating"])
        try:
            r_data = get_singular_restaurantdata(name)[0]
            r_id = r_data.id
            print(r_id)
            insert_rating(r_id, rating)
            return redirect(f"/restaurants/{name}")
        except Exception as e:
            return render_template("error.html", message="Ongelma arvion lisäämisessä palvelimelle")


@app.route("/<user>/restaurants")
def admin_restaurants_view(user):

    if session["admin"]:

        restaurant_data = get_main_restaurantdata(name=user)

        return render_template("restaurants_admin_view.html", restaurants = restaurant_data )
    
    else:

        return render_template("error.html", message="Sinulla ei ole oikeuksia päästä tälle sivulle :(")
    
@app.route("/<user>/restaurants/<restaurant_name>", methods = ["GET", "POST"])
def admin_restaurant_view(user, restaurant_name):

    restaurant, info, menu, messages = get_singular_restaurantdata(name=restaurant_name)

    if request.method == "GET":
        #The actual admin view of a single restaurant

        if session["admin"]:

            #Check that the restaurant belongs to the session user
            if restaurant.owner != session["user"]:
                return render_template("error.html", message="Sinulla ei ole oikeuksia päästä tälle sivulle :(")
            
            #Check that menu has items, change it to an empty list if it does not

            if menu[0][0] == None:
                menu = []


            return render_template("restaurant_admin_view.html", restaurant=restaurant, info=info, menu=menu)
        
        else:
            #I guess I could delete this later
            return render_template("error.html", message="Sinulla ei ole oikeuksia päästä tälle sivulle :(")
        
    else:
        #Handle updating the information of the restaurant.

        name = request.form["restaurant_name"]
        address = request.form["address"]
        city = request.form["city"]

        infotext = request.form["infotext"]
        open_times = request.form["open_times"]

        id = int(restaurant.id)

        try:
            update_restaurant_info(id, name, address, city, infotext, open_times)
        except Exception as e:
            return render_template("error.html", message=e)


        for key, value in request.form.items():
            if key.startswith("name_"):
                item_id = key.split("_")[1]
                food = value
                price = float(request.form.get(f"price_{item_id}"))
                deleteitem = request.form.get(f"{item_id}_delete")
                if deleteitem:
                    try:
                        delete_menuitem(item_id)
                    except:
                        raise ValueError(f"Error deleting {food} from the database")
                
                else:
                    #If we dont want to delete the item, we need to update its information to the database
                    try:
                        update_menu(item_id, food, price)
                    except Exception as e:
                        return render_template("error.html", message=e)
                
        newfood = request.form["menuitem"]
        newfood_price = request.form["menuitem_price"]

        if len(newfood) > 0 and len(newfood_price) > 0:
            newfood_price = float(newfood_price)
            if newfood_price > 0:
                try:
                    insert_menuitem(restaurant.id, newfood, newfood_price)
                except Exception as e:
                        return render_template("error.html", message=e)
            
        return redirect(f"/{session['user']}/restaurants/{restaurant.name}")

            

@app.route("/<user>/restaurants/<restaurant_name>/delete_restaurant", methods = ["GET", "POST"])
def delete_restaurant(user, restaurant_name):

    restaurant, info, menu, messages = get_singular_restaurantdata(name=restaurant_name)




        #Check that the restaurant belongs to the session user
    if restaurant.owner != session["user"]:
        return render_template("error.html", message="Sinulla ei ole oikeuksia päästä tälle sivulle :(")


    
    if request.method == "GET":
        return render_template("delete_restaurant.html", restaurant=restaurant)
        
    else:
        print("Here")
        should_delete = request.form.getlist("delete")

        print("Should?")
        

        if should_delete:
            try:
                delete_restaurant_from_db(restaurant.id)
                return redirect(f"/{session['user']}/restaurants")
            except Exception as e:
                return render_template("error.html", message=e)
            
        else:
            return redirect(f"/{session['user']}/restaurants/{restaurant.name}")





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
            token = session["csrf_token"]
            user_id = session["user_id"]
            name = request.form["name"]
            address = request.form["address"]
            city = request.form["city"]

            #Check that any field is not empty
            if not name or not address or not city:
                return redirect("/{session.user}/restaurants")

            create_new_restaurant(user_id, name, address, city, token, session)
            return redirect(f"/{session['user']}/restaurants")
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