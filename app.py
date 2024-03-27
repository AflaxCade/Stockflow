import jwt
import uuid
from functools import wraps
from datetime import datetime, timedelta
from config import app, db, bcrypt
from flask import make_response, request, jsonify
from models import Users, Customers, Suppliers, Categories, Products, Orders, OrderDetails


app.url_map.strict_slashes = False



def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/login', methods=['POST'])
def login():
    # auth = request.authorization
    # if not auth or not auth.username or not auth.password :
    #     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    # user = Users.query.filter_by(user_name=auth.username).first()

    data = request.get_json()
    if not data or not data['username'] or not data['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    
    user = Users.query.filter_by(user_name=data['username']).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    if bcrypt.check_password_hash(user.user_password, data['password']):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

# This route will return a user by their ID
@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_user(current_user,public_id):
    user = Users.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['user_name'] = user.user_name
    user_data['user_password'] = user.user_password
    user_data['user_email'] = user.user_email
    user_data['admin'] = user.admin
    return jsonify(user_data), 200


# This route will return all users
@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = Users.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['user_name'] = user.user_name
        user_data['user_password'] = user.user_password
        user_data['user_email'] = user.user_email
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output}), 200



# This route will create a new user
@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    data = request.get_json()

    user_name = data.get('user_name')
    user_password = data.get('user_password')
    user_email = data.get('user_email')

    if not user_name or not user_password or not user_email:
        return jsonify({'message': 'Username, password and email are required'}), 400

    existing_user = Users.query.filter_by(user_name=user_name).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')

    new_user = Users(
        public_id=str(uuid.uuid4()),
        user_name=user_name,
        user_password=hashed_password,
        user_email=user_email,
        admin=False
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


# This route will update a user
@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def update_user(current_user, public_id):

    if current_user.public_id != public_id:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    user = Users.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    if 'user_name' in data:
        user.user_name = data['user_name']
    if 'user_password' in data:
        user.user_password = bcrypt.generate_password_hash(data['user_password']).decode('utf-8')
    if 'user_email' in data:
        user.user_email = data['user_email']
    if not user.user_name or not user.user_password or not user.user_email:
        return jsonify({'message': 'Missing required value'}), 400

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200


# This route will promote a user to admin
@app.route('/promote/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user,public_id):
    if current_user.admin == False:
        return jsonify({'message': 'Cannot perform that function!'}), 403
    user = Users.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.admin = True
    db.session.commit()

    return jsonify({'message': 'User has been promoted to admin'}), 200

# This route will delete a user
@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if current_user.admin == False:
        return jsonify({'message': 'Cannot perform that function!'}), 403
    user = Users.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200


# This route will return a customer by their ID
@app.route("/customer/<customer_id>", methods=["GET"])
@token_required
def get_customer(current_user, customer_id):
    customer = Customers.query.filter_by(customer_id=customer_id).first()
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    customer_data = {}
    customer_data["customer_id"] = customer.customer_id
    customer_data["customer_name"] = customer.customer_name
    customer_data["customer_email"] = customer.customer_email
    customer_data["customer_phone"] = customer.customer_phone
    customer_data["customer_address"] = customer.customer_address
    customer_data["date"] = customer.date
    return jsonify(customer_data), 200


# This route will return all customers
@app.route("/customers", methods=["GET"])
@token_required
def get_all_customers(current_user):
    customers = Customers.query.all()
    output = []
    for customer in customers:
        customer_data = {}
        customer_data["customer_id"] = customer.customer_id
        customer_data["customer_name"] = customer.customer_name
        customer_data["customer_email"] = customer.customer_email
        customer_data["customer_phone"] = customer.customer_phone
        customer_data["customer_address"] = customer.customer_address
        customer_data["date"] = customer.date
        output.append(customer_data)
    return jsonify(output), 200


# This route will create a new customer
@app.route("/customers", methods=["POST"])
@token_required
def create_customer(current_user):
    data = request.get_json()
    customer_name=data["customer_name"]
    customer_email=data["customer_email"]
    customer_phone=data["customer_phone"]
    customer_address=data["customer_address"]

    if not customer_name or not customer_email or not customer_phone or not customer_address:
        return jsonify({"message": "You must include a name, email, phone and address"}), 400

    existing_customer = Customers.query.filter_by(customer_email=customer_email).first()
    if existing_customer:
        return jsonify({"message": "A customer with this email already exists"}), 400
    
    new_customer = Customers(
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        customer_address=customer_address)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "New customer created"}), 201


# This route will update a customer
@app.route("/customer/<customer_id>", methods=["PUT"])
@token_required
def update_customer(current_user, customer_id):
    customer = Customers.query.filter_by(customer_id=customer_id).first()
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    data = request.get_json()
    if "customer_name" in data:
        customer.customer_name = data["customer_name"]
    if "customer_email" in data:
        customer.customer_email = data["customer_email"]
    if "customer_phone" in data:
        customer.customer_phone = data["customer_phone"]
    if "customer_address" in data:
        customer.customer_address = data["customer_address"]
    if not customer.customer_name or not customer.customer_email or not customer.customer_phone or not customer.customer_address:
        return jsonify({"message": "Missing required value"}), 400
    db.session.commit()
    return jsonify({"message": "Customer updated"}), 200


# This route will delete a customer
@app.route("/customer/<customer_id>", methods=["DELETE"])
@token_required
def delete_customer(current_user, customer_id):
    customer = Customers.query.filter_by(customer_id=customer_id).first()
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 200


