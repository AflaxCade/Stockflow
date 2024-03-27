from config import db, bcrypt
from datetime import datetime


# Create a class for the Users table
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(60), unique=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)


# Create a class for the Customers table
class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False, unique=True)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
