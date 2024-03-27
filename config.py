from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Inventory.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "d84fc2bfa477fd5e850e86ae0a106d57"

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)