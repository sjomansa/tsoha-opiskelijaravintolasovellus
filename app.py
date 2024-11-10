from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_user", methods=["POST"])
def register_user():
    password = request.form["password1"]
    username = request.form["username"]

    #Look up if its a student or a restaurant
    status = request.form["admin"]

    admin = False
    if status == "ravintoloitsija":
        admin = True

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

        
