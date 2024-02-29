from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import orm_model, schema_model
from fastapi.responses import JSONResponse
from database_conn import *
orm_model.Base.metadata.create_all(bind=engine)
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Access environment variables
environment = os.getenv("ENVIRONMENT")
domain_name = os.getenv("DOMAIN_NAME")



