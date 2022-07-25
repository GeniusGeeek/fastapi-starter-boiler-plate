# fastapi-starter-boiler-plate
A starter boiler plate pack for developing apllications with FAST API 
This Boilerplate has basics utililities of software and saves the usersome development hassle.

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

1. Install fastapi and uvicorn server:
```bash 
install "fastapi[all]"
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
5. Install Requirements
```bash
pip3 install -r requirement.txt
```


## B. Start Application

1. Create database for application: eg. fastapi_starter_pack 
note: (do not create tables,running migrations willdo that)

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
127.0.0.1:8000  
127.0.0.1:8000/docs
