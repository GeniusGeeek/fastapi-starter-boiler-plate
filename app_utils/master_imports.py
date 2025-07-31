from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import orm_model, schema_model
from fastapi.responses import JSONResponse
from database_conn import *
orm_model.Base.metadata.create_all(bind=engine)
from dotenv import load_dotenv
import os
#bcrypt.__about__ = bcrypt
# or pip install "bcrypt==4.0.1" to fix bycrypt version issue


# Load environment variables from .env file
load_dotenv()
# Access environment variables
environment = os.getenv("ENVIRONMENT")
domain_name = os.getenv("DOMAIN_NAME")
email_password = os.getenv("EMAIL_PASSWORD")
email_host = os.getenv("EMAIL_HOST")
email_address = os.getenv("EMAIL_ADDRESS")
email_port = os.getenv("EMAIL_PORT")
some_api_keys = os.getenv("SOME_API_KEY")


