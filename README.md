# Foodics backend task

This project is an application built using FastAPI, SQLModel, and Docker. It handles orders, products, and ingredients, for a restaurant ordering and stock management system.

## Overview
This project assumes that the user is only one merchant, so authentication was excluded. This is for simplicity purposes. The project is containerized for ease of use. It has 2 routes only:
1. POST `/orders` to create orders and this is where the main flow of the app gets triggered.
2. GET `/orders` to list orders, which is not required in the task but is there for demonstration purposes only.
####
The app uses SQLmodel as an orm which is built on top of sqlalchemy and pydantic. It also uses
FastAPI as a web server.
####
All commands are best run through the provided MAKE file, it abstracts the interactions with the system through a series of pre-defined commands that makes it easier to interact with the app.
####
The app contains an auto-generated docs using swagger that can be used to try out the app routes.
####
The app structure was designed to go with a larger codebase for demonstration purposes.
####
Environment variables and secrets are included in the docker-compose file to make it easier to run the project without the hassle of creating a .env file on your machine, in typical production environment this should not be the case.

## Project Structure
```sh
├── Dockerfile
├── Dockerfile.test
├── README.md
├── __pycache__
│   └── main.cpython-312.pyc
├── app
│   ├── actions
│   │   ├── __init__.py
│   │   ├── ingredient.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── product.py
│   │   └── product_ingredient.py
│   ├── db.py
│   ├── dependencies.py
│   ├── errors.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── pydantic
│   │       ├── __init__.py
│   │       └── order.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── order.py
│   ├── scripts
│   │   ├── __init__.py
│   │   └── seed_db.py
│   ├── settings.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── actions
│   │   │   ├── __init__.py
│   │   │   ├── test_ingredient.py
│   │   │   ├── test_order.py
│   │   │   ├── test_order_item.py
│   │   │   └── test_product.py
│   │   ├── conftest.py
│   │   ├── models
│   │   │   └── __init__.py
│   │   └── routes
│   │       ├── __init__.py
│   │       └── test_order.py
│   └── utils
│       ├── __init__.py
│       │   └── sendgrid_email.cpython-312.pyc
│       └── send_email.py
├── docker-compose.debug.yml
├── docker-compose.test.yml
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── MAKE
└── pytest.ini
```
## Setup Instructions
### Prerequisites
Before you begin, ensure you have met the following requirements:
1. Docker & Docker Compose
2. Make

### Cloning the Repository
```bash
git clone git@github.com:abdelrahmenAyman/foodics-task.git
cd foodics-task
```
### Running the Project
To start the server, run:
```bash
make run
```
To start the server in detached mode (background):
```bash
make run-detached
```
### Running Tests
To run the test suite, execute:
```bash
make test
```
### Building Docker Images
To build the Docker image for the project:
```bash
make build
```
To build the Docker image for testing:
```bash
make build-test
```
### Stopping and Cleaning Up Containers
To stop all running containers:
```bash
make stop
```
To remove all containers, networks, and volumes:
```bash
make down
```
### Seeding the Database
To seed the database with initial data, run:
1. Make sure you have the compose service up first.
2. Run the following command
```bash
make seed-db
```
Dropping the Database
To drop the database and remove the data volume:
```bash
make drop-db
```
## Accessing API Documentation
To access the API documentation, navigate to:
http://localhost:8000/docs
This will provide interactive documentation of your API using Swagger.
