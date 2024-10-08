![License](https://img.shields.io/badge/license-MIT-green) <img src="https://img.shields.io/circleci/project/github/badges/shields/master" alt="build status">
# fastapi-starter-boiler-plate
A starter boiler plate pack for developing apllications endpoints with FAST API. 
This Boilerplate has basics utililities needed for building REST APIs without much hassle and saves the user some development hassle.

## Features includes:

- Registration
- User Login
- CORS
- Reset Password
- Forgot Password
- Authentication and Protected Routes (JWT)
- Getting Autheticated User Details
- Google Authentication
- Email/Account Verification
- Edit Account/Profile
- Email Sending
- Password hashing
- User Account hashing
- File Upload and Download
- Reusable examples for routes and CRUD/Model operations setup
- CRUD model operations cheat sheet
  
 

## Installation

```bash
git clone https://github.com/GeniusGeeek/fastapi-starter-boiler-plate.git
```

## A. REQUIMENTS
#Python 3.6 and greater



In project directory run the following two commands to create a virtual environment
```bash
pip3 install --upgrade pip 
python3 -m venv .env 
```
```bash
source .env/bin/activate
```

1. Install fastapi and uvicorn server:
```bash 
pip3 install "fastapi[all]"
```

2. Install SQLAlchemy for ORM management
```bash 
pip3 install SQLAlchemy
```
3.  Install Mysql connection for python (note: This is a mySQL driver, you will need to install the driver for other databases you want to use that's not mySQL) 
```bash 
pip3 install mysql-connector-python
```
4. Install Alembic for Database Migrations
```bash 
pip3 install alembic
```
5. Install other Requirements (note: if you have errors in installing any of the requirements you may either remove version specification or use a VPN. You may also comment out the package if it is not a core FastAPI Package)
```bash
pip3 install -r requirements.txt
```



## B. Start Application

1. Create database for application: eg. fastapi_starter_pack 
note: (do not create tables,running migrations will do that)

2. Run database migrations
```bash
alembic revision --autogenerate -m "initial setup"
alembic upgrade head
```

3. OPTIONAL: change DB url definations in database_conn.py and alembic.ini if needed according to your db name and settings


4. Run Application
```bash
uvicorn main:app --reload 
```

6. visit url in browser

      127.0.0.1:8000,  
      127.0.0.1:8000/docs
