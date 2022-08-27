![License](https://img.shields.io/badge/license-MIT-green) <img src="https://img.shields.io/circleci/project/github/badges/shields/master" alt="build status">
# fastapi-starter-boiler-plate
A starter boiler plate pack for developing apllications endpoints with FAST API 
This Boilerplate has basics utililities of software and saves the user some development hassle.

## Features includes:

- Registration
- User Login
- CORS
- Reset Password
- Forgot Password
- Authentication (JWT)
- Email Sending
- Password hashing
- User Account hashing 

## Installation

## A. REQUIMENTS
#Python 3.6 and greater

In project directory run the following two commands to create a virtual environment
```bash
python3 -m venv .env 
```
```bash
source .env/bin/activate
```

1. Install fastapi and uvicorn server:
```bash 
pip install "fastapi[all]"
```

2. Install SQLAlchemy for ORM management
```bash 
pip install SQLAlchemy
```
3.  Install Mysql connection for python 
```bash 
pip install mysql-connector-python
```
4. Install Alembic for Database Migrations
```bash 
pip install alembic
```
5. Install other Requirements
```bash
pip install -r requirement.txt
```


## B. Start Application

1. Create database for application: eg. fastapi_starter_pack 
note: (do not create tables,running migrations will do that)

2. Run database migrations
```bash
alembic revision --autogenerate -m "initial setup"
alembic upgrade head
```

3. OPTIONAL: change DB url definations if needed according to your db name and settings


4. Run Application
```bash
uvicorn main:app --reload 
```

6. visit url in browser

      127.0.0.1:8000,  
      127.0.0.1:8000/docs
