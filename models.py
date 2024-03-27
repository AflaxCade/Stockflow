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


# create a class for the Suppliers table
class Suppliers(db.Model):
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    supplier_email = db.Column(db.String(100), nullable=False, unique=True)
    supplier_phone = db.Column(db.String(20), nullable=False)
    supplier_address = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# Create a class for the Categories table
class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    category_description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# Create a class for the Products table
class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# Create a class for the Orders table
class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expected_delivery_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    order_details = db.relationship('OrderDetails', backref='order', lazy=True)


# Create a class for the OrderDetails table
class OrderDetails(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity_ordered  = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
