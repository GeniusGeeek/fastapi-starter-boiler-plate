RUN THE FOLLOWING COMMANDS TO GET STARTED:

A. REQUIMENTS
Python 3.6 and greater

In project directory run the following two commands to create a virtual environment
**pip3 install --upgrade pip 
**python3 -m venv .env 
**source .env/bin/activate  

1. Install fastapi and uvicorn server:
** pip3 install "fastapi[all]"

2. Install SQLAlchemy for ORM management
** pip3 install SQLAlchemy

3.  Install Mysql connection for python (note: This is a mySQL driver, you will need to install the driver for other databases you want to use that's not mySQL) 
** pip3 install mysql-connector-python

4. Install Alembic for Database Migrations
** pip3 install alembic
** alembic init alembic --generates a new alembic directory

B. Start Application

1. Create database for application: eg. fastapi_starter_pack 
note: (do not create tables,running migrations willdo that)

2. Run database migrations
** alembic revision --autogenerate -m "initial setup"
** alembic upgrade head

3. OPTIONAL: change DB url definations in database_conn.py and alembic.ini if needed according to your db name and settings

4. Install Requirements
** pip3 install -r requirements.txt

5. Run Application
** uvicorn main:app --reload 

6. visit url
** 127.0.0.1:8000 in browser 
** 127.0.0.1:8000/docs in browser to test api out
