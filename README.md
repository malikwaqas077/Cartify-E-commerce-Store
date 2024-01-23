# Cartify An E-commerce Store

## Introduction

FlaskDataApp is a Flask-based web application designed to manage an e-commerce platform. The application features user registration, product management, cart functionalities, and payment processing.

## Features

- **User Management:** Includes user registration and login functionalities.
- **Product Management:** Allows adding, editing, and deleting products. It utilizes a MySQL database to store product details like name, description, and price.
- **Shopping Cart:** Users can add products to their cart and view their cart contents.
- **Payment Processing:** Implements a basic payment form where users can input their payment details.

## Installation and Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/malikwaqas077/FlaskDataApp.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

   This will install Flask, WTForms, MySQLdb, SQLAlchemy, and other necessary packages.

3. Configure MySQL database settings in `FlaskDataApp.py` to match your database credentials.

## Running the Application

Execute the following command in the project directory:

```bash
python FlaskDataApp.py

```
The application will start running on localhost at the specified port.
## Modules Overview

- `FlaskDataApp.py`: The main application file containing Flask routes and configurations.
- `UserDashboard.py`: Handles user dashboard functionalities.
- `dashboard.py`: Manages the product dashboard.
- `forms.py`: Contains WTForms forms for product and user handling.
- `models.py`: Defines SQLAlchemy models for the database.
- `payment.py`: Implements payment functionalities.
- `product_routes.py`: Manages routes related to product operations.

## Contributing

Contributions to the FlaskDataApp are welcome. Please ensure to follow the standard practices for code contribution and make pull requests for any changes.

This markdown structure includes headings, bullet points, and code blocks, making it clear and readable for GitHub viewers.
