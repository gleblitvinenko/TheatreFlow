# Theatre-API-Service

Theatre-API-Service is a Python Django REST framework (DRF) based API service for managing data related to a theater. It provides endpoints to manage actors, genres, theater halls, plays, performances, and reservations.

## Features

- CRUD operations for managing actors, genres, theater halls, plays, performances, and reservations.
- Role-based authentication with admin and user roles.
- API documentation using the Django Rest Framework's built-in schema generation.
- User authentication and authorization using JWT (JSON Web Tokens).
- Uploading and managing play images.
- Seat validation based on the theatre hall's capacity when creating tickets.
- Dockerized for easy deployment and scaling.

## Prerequisites

To run the Theatre-API-Service, you need the following prerequisites:

- Python 3.x
- Django 3.x
- Django REST framework 3.x
- Other dependencies listed in the `requirements.txt` file.

Before running the Theatre API service in Docker, ensure you have the following installed on your machine:

- Docker: Install Docker
- Docker Compose: Install Docker Compose

## Getting Started

Follow these steps to set up and run the Theatre-API-Service locally:

1. Clone the repository:

`git clone https://github.com/gleblitvinenko/Theatre-API-Service.git
cd Theatre-API-Service`


2. Create and activate a virtual environment (optional but recommended):

`python -m venv venv`

`source venv/bin/activate`

On Windows:

`venv\Scripts\activate`


3. Install dependencies:

`pip install -r requirements.txt`


4. Set up the database:

`python manage.py migrate`


5. Create a superuser (admin):

`python manage.py createsuperuser`


6. Run the development server:

`python manage.py runserver`


7. Open the API documentation in your browser:

`http://localhost:8000/api/doc/swagger/`


## Environment Variables

The Theatre-API-Service uses the following environment variables:

- `SECRET_KEY`: Django secret key for secure data. (Default: `secret_key`)
- `DEBUG`: Set to `True` for development and `False` for production. (Default: `True`)

Make sure to configure these environment variables before running the application. You can use a `.env` file to set these variables.

### .env_sample file

A file named .env_sample is included in the repository as a template for setting up the .env file. It contains the names of the environment variables without their values. You can use it as a reference when creating your own .env file.

## API Documentation

The API documentation is automatically generated using Django Rest Framework's built-in schema generation. You can access the API documentation by running the development server and visiting the following URL:

`http://localhost:8000/api/doc/swagger/`


The documentation provides detailed information about each API endpoint, including available methods, request parameters, response formats, and authentication requirements.

Feel free to explore the API documentation to understand the available endpoints and how to interact with the Theatre-API-Service.

## Authentication

The API service uses JWT for user authentication. To access protected endpoints, include the JWT token in the Authorization header as follows:

`Authorization: Bearer your_jwt_token`

To obtain a JWT token, make a POST request to /api/user/token/ with your email and password.

---

Thank you for using Theatre-API-Service!