# Stockflow

StockFlow is a sophisticated and agile inventory management system designed to streamline and optimize the tracking, control, and organization of products within a business. Leveraging the power of Python Flask, StockFlow provides a seamless and efficient experience through its RESTful API, offering a comprehensive solution for businesses of all sizes.

## Table of Contents
- [Features](#features)
- [Technology Used](#Technologies-Used)
- [Installation](#Installation)
  - [Requirements](#Requirements)
- [API Endpoints](#API-Endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

#### User Management
- Authentication and authorization using JWT tokens.
- User CRUD operations: Create, Read, Update, Delete.

#### Customer Management
- Customer CRUD operations: Create, Read, Update, Delete.

#### Supplier Management
- Supplier CRUD operations: Create, Read, Update, Delete.

#### Category Management
- Category CRUD operations: Create, Read, Update, Delete.

#### Product Management
- Product CRUD operations: Create, Read, Update, Delete.

#### Order Management
- Order CRUD operations: Create, Read, Update.
- Order Detail CRUD operations: Read, Update.

## Technologies Used

- Flask: A Python web framework for building web applications.
- UUID: A module for generating universally unique identifiers.
- Bcrypt: A password hashing function used for securely storing user passwords.
- SQLAlchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library.
- RESTful API: Enables communication and data exchange between the frontend and backend.
- SQLite: A lightweight and easy-to-use relational database used for storing contact information.
- JWT (JSON Web Tokens): A standard for securely transmitting information between parties as a JSON object.

## Installation

### Requirements

- Python 3.x
- pip

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/AflaxCade/Stockflow.git
```

2. Navigate to the project directory:

```bash
cd Stockflow
```

3. Create a virtual environment:

```bash
python -m venv env
```

4. Activate the virtual environment:

- For Windows:

```bash
env\Scripts\activate
```

- For macOS and Linux:

```bash
source env/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
python app.py
```

The server will start on `http://localhost:5000`.

## API Endpoints

The application provides several API endpoints for managing resources. You will need to use a tool like Postman or curl to interact with these endpoints.

**Note:** Endpoints require a JWT token for authentication. You can obtain a token by logging in.

This document outlines the endpoints available in the API along with their functionalities.

## Authentication

The following endpoint handles user authentication:

### Login

- **URL**: `/login`
- **Method**: `POST`
- **Description**: Authenticates users and generates a JWT token.
- **Request Body**:
  ```json
  {
      "username": "admin",
      "password": "admin"
  }
  ```
- **Response**: Returns a JWT token upon successful authentication.

[Example about login endpoint click here](https://documenter.getpostman.com/view/33172740/2sA35EZ2bC)

## User Management

Endpoints related to managing users.

### Get User by ID

- **URL**: `/user/<public_id>`
- **Method**: `GET`
- **Description**: Retrieves user details by their ID.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns user details in JSON format.

### Get All Users

- **URL**: `/users`
- **Method**: `GET`
- **Description**: Retrieves details of all users.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a list of users in JSON format.

### Create User

- **URL**: `/user`
- **Method**: `POST`
- **Description**: Creates a new user.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "user_name": "string",
      "user_password": "string",
      "user_email": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Update User

- **URL**: `/user/<public_id>`
- **Method**: `PUT`
- **Description**: Updates user details.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "user_name": "string",
      "user_password": "string",
      "user_email": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Promote User to Admin

- **URL**: `/promote/<public_id>`
- **Method**: `PUT`
- **Description**: Promotes a user to admin status.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a message indicating success or failure.

### Delete User

- **URL**: `/user/<public_id>`
- **Method**: `DELETE`
- **Description**: Deletes a user.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a message indicating success or failure.

[For more examples about User management endpoints click here](https://documenter.getpostman.com/view/33172740/2sA35EYhZi)

# Customer Management

Endpoints related to managing customers.

### Get Customer by ID

- **URL**: `/customer/<customer_id>`
- **Method**: `GET`
- **Description**: Retrieves customer details by their ID.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns customer details in JSON format.

### Get All Customers

- **URL**: `/customers`
- **Method**: `GET`
- **Description**: Retrieves details of all customers.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a list of customers in JSON format.

### Create Customer

- **URL**: `/customers`
- **Method**: `POST`
- **Description**: Creates a new customer.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "customer_name": "string",
      "customer_email": "string",
      "customer_phone": "string",
      "customer_address": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Update Customer

- **URL**: `/customer/<customer_id>`
- **Method**: `PUT`
- **Description**: Updates customer details.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "customer_name": "string",
      "customer_email": "string",
      "customer_phone": "string",
      "customer_address": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Delete Customer

- **URL**: `/customer/<customer_id>`
- **Method**: `DELETE`
- **Description**: Deletes a customer.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a message indicating success or failure.

[For more examples about Customer management endpoints click here](https://documenter.getpostman.com/view/33172740/2sA35D43An)

## Supplier Management

Endpoints related to managing suppliers.

### Get Supplier by ID

- **URL**: `/supplier/<supplier_id>`
- **Method**: `GET`
- **Description**: Retrieves supplier details by their ID.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns supplier details in JSON format.

### Get All Suppliers

- **URL**: `/suppliers`
- **Method**: `GET`
- **Description**: Retrieves details of all suppliers.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a list of suppliers in JSON format.

### Create Supplier

- **URL**: `/suppliers`
- **Method**: `POST`
- **Description**: Creates a new supplier.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "supplier_name": "string",
      "supplier_email": "string",
      "supplier_phone": "string",
      "supplier_address": "string",
      "country": "string",
      "state": "string",
      "city": "string",
      "zip_code": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Update Supplier

- **URL**: `/supplier/<supplier_id>`
- **Method**: `PUT`
- **Description**: Updates supplier details.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "supplier_name": "string",
      "supplier_email": "string",
      "supplier_phone": "string",
      "supplier_address": "string",
      "country": "string",
      "state": "string",
      "city": "string",
      "zip_code": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Delete Supplier

- **URL**: `/supplier/<supplier_id>`
- **Method**: `DELETE`
- **Description**: Deletes a supplier.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a message indicating success or failure.

[For more examples about Supplier management endpoints click here](https://documenter.getpostman.com/view/33172740/2sA35EZNgY)

## Category Management

Endpoints related to managing categories.

### Get Category by ID

- **URL**: `/category/<category_id>`
- **Method**: `GET`
- **Description**: Retrieves category details by its ID.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns category details in JSON format.

### Get All Categories

- **URL**: `/categories`
- **Method**: `GET`
- **Description**: Retrieves details of all categories.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a list of categories in JSON format.

### Create Category

- **URL**: `/categories`
- **Method**: `POST`
- **Description**: Creates a new category.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "category_name": "string",
      "category_description": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Update Category

- **URL**: `/category/<category_id>`
- **Method**: `PUT`
- **Description**: Updates category details.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "category_name": "string",
      "category_description": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Delete Category

- **URL**: `/category/<category_id>`
- **Method**: `DELETE`
- **Description**: Deletes a category.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a message indicating success or failure.

[For more examples about Category management endpoints click here](https://documenter.getpostman.com/view/33172740/2sA35EZhZ2)

# Product Management

Endpoints related to managing products.

### Get Product by ID

- **URL**: `/product/<product_id>`
- **Method**: `GET`
- **Description**: Retrieves product details by its ID.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns product details in JSON format.

### Get All Products

- **URL**: `/products`
- **Method**: `GET`
- **Description**: Retrieves details of all products.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a list of products in JSON format.

### Create Product

- **URL**: `/products`
- **Method**: `POST`
- **Description**: Creates a new product.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "product_name": "string",
      "product_description": "string",
      "product_price": "string",
      "product_quantity": "string",
      "category_id": "string",
      "supplier_id": "string"
  }
  ```
  - **Response**: Returns a message indicating success or failure.

  ### Update Product

- **URL**: `/product/<product_id>`
- **Method**: `PUT`
- **Description**: Updates product details.
- **Request Headers**: Requires a valid JWT token.
- **Request Body**:
  ```json
  {
      "product_name": "string",
      "product_description": "string",
      "product_price": "string",
      "product_quantity": "string",
      "category_id": "string",
      "supplier_id": "string"
  }
  ```
- **Response**: Returns a message indicating success or failure.

### Delete Product

- **URL**: `/product/<product_id>`
- **Method**: `DELETE`
- **Description**: Deletes a product.
- **Request Headers**: Requires a valid JWT token.
- **Response**: Returns a message indicating success or failure.

[For more examples about Product management endpoints click here](https://documenter.getpostman.com/view/33172740/2sA35EZi1V)

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Create a new Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
