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
