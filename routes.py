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
    
    except Exception as e:
        return render_template("error.html", message=e) #Add more detailed error message here
    

@app.route("/logout")
def logout():

    logout_user(session)
    return redirect("/")



#Main restaurant view of opiskelijaravintolat, where you can see the list of all restaurants
@app.route("/restaurants", methods=["GET", "POST"] )
def restaurants_view():

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

    try:
        restaurant, info, menu, messages = get_singular_restaurantdata(name)
    except:
        return render_template("error.html", message = "Ravintolaa ei löydy, oletko varma, että tämän niminen ravintola on olemassa?")

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
        try:
            rating = int(request.form["rating"])
        except:
            return render_template("error.html", message="Syötä arvo väliltä 1-5")
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
        token = request.form["csrf_token"]

        infotext = request.form["infotext"]
        open_times = request.form["open_times"]

        id = int(restaurant.id)

        if token != session["csrf_token"]:
            return render_template("error.html", message="Virhe tietojen muokkaamisessa, sinun CSRF-token ei ole sama kuin käyttäjällä!")

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

        should_delete = request.form.getlist("delete")
        token = request.form["csrf_token"]
        
        if should_delete:
            try:
                delete_restaurant_from_db(restaurant.id, token, session)
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

