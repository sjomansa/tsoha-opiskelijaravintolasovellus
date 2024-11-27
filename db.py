from app import app
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import secrets

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
