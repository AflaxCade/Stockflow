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


# This route will return a supplier by their ID
@app.route("/supplier/<supplier_id>", methods=["GET"])
@token_required
def get_supplier(current_user, supplier_id):
    supplier = Suppliers.query.filter_by(supplier_id=supplier_id).first()
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    supplier_data = {}
    supplier_data["supplier_id"] = supplier.supplier_id
    supplier_data["supplier_name"] = supplier.supplier_name
    supplier_data["supplier_email"] = supplier.supplier_email
    supplier_data["supplier_phone"] = supplier.supplier_phone
    supplier_data["supplier_address"] = supplier.supplier_address
    supplier_data["country"] = supplier.country
    supplier_data["state"] = supplier.state
    supplier_data["city"] = supplier.city
    supplier_data["zip_code"] = supplier.zip_code
    supplier_data["date"] = supplier.date
    return jsonify(supplier_data), 200


# This route will return all suppliers
@app.route("/suppliers", methods=["GET"])
@token_required
def get_all_suppliers(current_user):
    suppliers = Suppliers.query.all()
    output = []
    for supplier in suppliers:
        supplier_data = {}
        supplier_data["supplier_id"] = supplier.supplier_id
        supplier_data["supplier_name"] = supplier.supplier_name
        supplier_data["supplier_email"] = supplier.supplier_email
        supplier_data["supplier_phone"] = supplier.supplier_phone
        supplier_data["supplier_address"] = supplier.supplier_address
        supplier_data["country"] = supplier.country
        supplier_data["state"] = supplier.state
        supplier_data["city"] = supplier.city
        supplier_data["zip_code"] = supplier.zip_code
        supplier_data["date"] = supplier.date
        output.append(supplier_data)
    return jsonify(output), 200


# This route will create a new supplier
@app.route("/suppliers", methods=["POST"])
@token_required
def create_supplier(current_user):
    data = request.get_json()
    supplier_name=data["supplier_name"]
    supplier_email=data["supplier_email"]
    supplier_phone=data["supplier_phone"]
    supplier_address=data["supplier_address"]
    country=data["country"]
    state=data["state"]
    city=data["city"]
    zip_code=data["zip_code"]

    if not supplier_name or not supplier_email or not supplier_phone or not supplier_address or not country or not state or not city or not zip_code:
        return jsonify({"message": "You must include a name, email, phone, address, country, state, city and zip code"}), 400

    existing_supplier = Suppliers.query.filter_by(supplier_email=supplier_email).first()
    if existing_supplier:
        return jsonify({"message": "A supplier with this email already exists"}), 400
    
    new_supplier = Suppliers(
        supplier_name=supplier_name,
        supplier_email=supplier_email,
        supplier_phone=supplier_phone,
        supplier_address=supplier_address,
        country=country,
        state=state,
        city=city,
        zip_code=zip_code)
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({"message": "New supplier created"}), 201


# This route will update a supplier
@app.route("/supplier/<supplier_id>", methods=["PUT"])
@token_required
def update_supplier(current_user, supplier_id):
    supplier = Suppliers.query.filter_by(supplier_id=supplier_id).first()
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    data = request.get_json()
    if "supplier_name" in data:
        supplier.supplier_name = data["supplier_name"]
    if "supplier_email" in data:
        supplier.supplier_email = data["supplier_email"]
    if "supplier_phone" in data:
        supplier.supplier_phone = data["supplier_phone"]
    if "supplier_address" in data:
        supplier.supplier_address = data["supplier_address"]
    if "country" in data:
        supplier.country = data["country"]
    if "state" in data:
        supplier.state = data["state"]
    if "city" in data:
        supplier.city = data["city"]
    if "zip_code" in data:
        supplier.zip_code = data["zip_code"]
    if not supplier.supplier_name or not supplier.supplier_email or not supplier.supplier_phone or not supplier.supplier_address or not supplier.country or not supplier.state or not supplier.city or not supplier.zip_code:
        return jsonify({"message": "Missing required value"}), 400
    db.session.commit()
    return jsonify({"message": "Supplier updated"}), 200


# This route will delete a supplier
@app.route("/supplier/<supplier_id>", methods=["DELETE"])
@token_required
def delete_supplier(current_user,supplier_id):
    supplier = Suppliers.query.filter_by(supplier_id=supplier_id).first()
    if not supplier:
        return jsonify({"message": "Supplier not found"}), 404
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({"message": "Supplier deleted"}), 200


# This route will return a category by their ID
@app.route("/category/<category_id>", methods=["GET"])
@token_required
def get_category(current_user, category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404
    category_data = {}
    category_data["category_id"] = category.category_id
    category_data["category_name"] = category.category_name
    category_data["category_description"] = category.category_description
    category_data["date"] = category.date
    return jsonify(category_data), 200


# This route will return all categories
@app.route("/categories", methods=["GET"])
@token_required
def get_all_categories(current_user):
    categories = Categories.query.all()
    output = []
    for category in categories:
        category_data = {}
        category_data["category_id"] = category.category_id
        category_data["category_name"] = category.category_name
        category_data["category_description"] = category.category_description
        category_data["date"] = category.date
        output.append(category_data)
    return jsonify(output), 200


# This route will create a new category
@app.route("/categories", methods=["POST"])
@token_required
def create_category(current_user):
    data = request.get_json()
    category_name=data["category_name"]
    category_description=data["category_description"]

    if not category_name or not category_description:
        return jsonify({"message": "You must include a name and description"}), 400

    existing_category = Categories.query.filter_by(category_name=category_name).first()
    if existing_category:
        return jsonify({"message": "A category with this name already exists"}), 400
    
    new_category = Categories(
        category_name=category_name,
        category_description=category_description)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "New category created"}), 201


# This route will update a category
@app.route("/category/<category_id>", methods=["PUT"])
@token_required
def update_category(current_user, category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404
    data = request.get_json()
    if "category_name" in data:
        category.category_name = data["category_name"]
    if "category_description" in data:
        category.category_description = data["category_description"]
    if not category.category_name or not category.category_description:
        return jsonify({"message": "Missing required value"}), 400
    db.session.commit()
    return jsonify({"message": "Category updated"}), 200


# This route will delete a category
@app.route("/category/<category_id>", methods=["DELETE"])
@token_required
def delete_category(current_user, category_id):
    category = Categories.query.filter_by(category_id=category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


# This route will return a product by their ID
@app.route("/product/<product_id>", methods=["GET"])
@token_required
def get_product(current_user, product_id):
    product = Products.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"message": "Product not found"}), 404
    product_data = {}
    product_data["product_id"] = product.product_id
    product_data["product_name"] = product.product_name
    product_data["product_description"] = product.product_description
    product_data["product_price"] = product.product_price
    product_data["product_quantity"] = product.product_quantity
    product_data["category_id"] = product.category_id
    product_data["supplier_id"] = product.supplier_id
    product_data["date"] = product.date
    return jsonify(product_data), 200


# This route will return all products
@app.route("/products", methods=["GET"])
@token_required
def get_all_products(current_user):
    products = Products.query.all()
    output = []
    for product in products:
        product_data = {}
        product_data["product_id"] = product.product_id
        product_data["product_name"] = product.product_name
        product_data["product_description"] = product.product_description
        product_data["product_price"] = product.product_price
        product_data["product_quantity"] = product.product_quantity
        product_data["category_id"] = product.category_id
        product_data["supplier_id"] = product.supplier_id
        product_data["date"] = product.date
        output.append(product_data)
    return jsonify(output), 200


# This route will create a new product
@app.route("/products", methods=["POST"])
@token_required
def create_product(current_user):
    data = request.get_json()
    product_name=data["product_name"]
    product_description=data["product_description"]
    product_price=data["product_price"]
    product_quantity=data["product_quantity"]
    category_id=data["category_id"]
    supplier_id=data["supplier_id"]

    if not product_name or not product_description or not product_price or not product_quantity or not category_id or not supplier_id:
        return jsonify({"message": "You must include a name, description, price, quantity, category ID and supplier ID"}), 400

    existing_product = Products.query.filter_by(product_name=product_name).first()
    if existing_product:
        return jsonify({"message": "A product with this name already exists"}), 400
    
    new_product = Products(
        product_name=product_name,
        product_description=product_description,
        product_price=product_price,
        product_quantity=product_quantity,
        category_id=category_id,
        supplier_id=supplier_id)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "New product created"}), 201


# This route will update a product
@app.route("/product/<product_id>", methods=["PUT"])
@token_required
def update_product(current_user, product_id):
    product = Products.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"message": "Product not found"}), 404
    data = request.get_json()
    if "product_name" in data and data["product_name"]:
        product.product_name = data["product_name"]
    if "product_description" in data and data["product_description"]:
        product.product_description = data["product_description"]
    if "product_price" in data and data["product_price"]:
        product.product_price = data["product_price"]
    if "product_quantity" in data and data["product_quantity"]:
        product.product_quantity = data["product_quantity"]
    if "category_id" in data and data["category_id"]:
        product.category_id = data["category_id"]
    if "supplier_id" in data and data["supplier_id"]:
        product.supplier_id = data["supplier_id"]
    if not product.product_name or not product.product_description or not product.product_price or not product.product_quantity or not product.category_id or not product.supplier_id:
        return jsonify({"message": "Missing required value"}), 400

    db.session.commit()
    return jsonify({"message": "Product updated"}), 200


# This route will delete a product
@app.route("/product/<product_id>", methods=["DELETE"])
@token_required
def delete_product(current_user, product_id):
    product = Products.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"message": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200


# This route will return an order by its ID
@app.route('/order/<order_id>', methods=['GET'])
@token_required
def get_order(current_user, order_id):
    order = Orders.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    order_dict = {
        'order_id': order.order_id,
        'customer_id': order.customer_id,
        'order_date': order.order_date,
        'expected_delivery_date': order.expected_delivery_date,
        'status': order.status,
        'order_details': []
    }

    order_details = OrderDetails.query.filter_by(order_id=order.order_id).all()
    for detail in order_details:
        detail_dict = {
            'order_detail_id': detail.order_detail_id,
            'product_id': detail.product_id,
            'quantity_ordered': detail.quantity_ordered,
            'unit_price': detail.unit_price,
            'total_amount': detail.total_amount,
            'date': detail.date
        }
        order_dict['order_details'].append(detail_dict)

    return jsonify(order_dict), 200


# This route will return all orders
@app.route('/orders', methods=['GET'])
@token_required
def get_orders(current_user):
    orders = Orders.query.all()
    order_list = []

    for order in orders:
        order_dict = {
            'order_id': order.order_id,
            'customer_id': order.customer_id,
            'order_date': order.order_date,
            'expected_delivery_date': order.expected_delivery_date,
            'status': order.status,
            'order_details': []
        }

        order_details = OrderDetails.query.filter_by(order_id=order.order_id).all()
        for detail in order_details:
            detail_dict = {
                'order_detail_id': detail.order_detail_id,
                'product_id': detail.product_id,
                'quantity_ordered': detail.quantity_ordered,
                'unit_price': detail.unit_price,
                'total_amount': detail.total_amount,
                'date': detail.date
            }
            order_dict['order_details'].append(detail_dict)

        order_list.append(order_dict)

    return jsonify(order_list), 200


# This route will create a new order
@app.route('/orders', methods=['POST'])
@token_required
def create_order(current_user):
    data = request.get_json()

    required_fields = ['customer_id', 'order_date', 'expected_delivery_date', 'status', 'order_details']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    customer_id = data['customer_id']
    order_date = datetime.strptime(data['order_date'], '%Y-%m-%d %H:%M:%S')
    expected_delivery_date = datetime.strptime(data['expected_delivery_date'], '%Y-%m-%d %H:%M:%S')
    status = data['status']
    order_details = data['order_details']

    order = Orders(
        customer_id=customer_id,
        order_date=order_date,
        expected_delivery_date=expected_delivery_date,
        status=status
    )
    db.session.add(order)
    db.session.commit()

    for detail in order_details:

        required_detail_fields = ['product_id', 'quantity_ordered', 'unit_price', 'total_amount']
        for field in required_detail_fields:
            if field not in detail:
                return jsonify({'message': f'Missing required field in order details: {field}'}), 400
        
        product_id = detail['product_id']
        quantity_ordered = detail['quantity_ordered']
        unit_price = detail['unit_price']
        total_amount = detail['total_amount']

        order_detail = OrderDetails(
            order_id=order.order_id,
            product_id=product_id,
            quantity_ordered=quantity_ordered,
            unit_price=unit_price,
            total_amount=total_amount
        )
        db.session.add(order_detail)
        db.session.commit()

    return jsonify({'message': 'Order created successfully'}), 201


# this route will update an order
@app.route('/order/<order_id>', methods=['PUT'])
@token_required
def update_order(current_user, order_id):
    order = Orders.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    data = request.get_json()

    if 'customer_id' in data:
        order.customer_id = data['customer_id']
    if 'order_date' in data:
        order.order_date = datetime.strptime(data['order_date'], '%Y-%m-%d %H:%M:%S')
    if 'expected_delivery_date' in data:
        order.expected_delivery_date = datetime.strptime(data['expected_delivery_date'], '%Y-%m-%d %H:%M:%S')
    if 'status' in data:
        order.status = data['status']

    if not order.customer_id or not order.order_date or not order.expected_delivery_date or not order.status:
        return jsonify({'message': 'Missing required value'}), 400

    db.session.commit()

    return jsonify({'message': 'Order updated successfully'}), 200


# This route will return an order detail by its ID
@app.route('/order_detail/<order_detail_id>', methods=['GET'])
@token_required
def get_order_detail(current_user, order_detail_id):
    order_detail = OrderDetails.query.filter_by(order_detail_id=order_detail_id).first()
    if not order_detail:
        return jsonify({'message': 'Order detail not found'}), 404

    detail_dict = {
        'order_detail_id': order_detail.order_detail_id,
        'order_id': order_detail.order_id,
        'product_id': order_detail.product_id,
        'quantity_ordered': order_detail.quantity_ordered,
        'unit_price': order_detail.unit_price,
        'total_amount': order_detail.total_amount,
        'date': order_detail.date
    }

    return jsonify(detail_dict), 200

# This route will return all order details
@app.route('/order_details', methods=['GET'])
@token_required
def get_order_details(current_user):
    order_details = OrderDetails.query.all()
    output = []

    for detail in order_details:
        detail_dict = {
            'order_detail_id': detail.order_detail_id,
            'order_id': detail.order_id,
            'product_id': detail.product_id,
            'quantity_ordered': detail.quantity_ordered,
            'unit_price': detail.unit_price,
            'total_amount': detail.total_amount,
            'date': detail.date
        }
        output.append(detail_dict)

    return jsonify(output), 200


# this route will update an order detail
@app.route('/order_detail/<order_detail_id>', methods=['PUT'])
@token_required
def update_order_detail(current_user, order_detail_id):
    order_detail = OrderDetails.query.filter_by(order_detail_id=order_detail_id).first()
    if not order_detail:
        return jsonify({'message': 'Order detail not found'}), 404

    data = request.get_json()

    if 'order_id' in data:
        order_detail.order_id = data['order_id']
    if 'product_id' in data:
        order_detail.product_id = data['product_id']
    if 'quantity_ordered' in data:
        order_detail.quantity_ordered = data['quantity_ordered']
    if 'unit_price' in data:
        order_detail.unit_price = data['unit_price']
    if 'total_amount' in data:
        order_detail.total_amount = data['total_amount']

    if not order_detail.order_id or not order_detail.product_id or not order_detail.quantity_ordered or not order_detail.unit_price or not order_detail.total_amount:
        return jsonify({'message': 'Missing required value'}), 400

    db.session.commit()

    return jsonify({'message': 'Order detail updated successfully'}), 200



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
