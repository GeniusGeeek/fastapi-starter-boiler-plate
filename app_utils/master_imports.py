from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import orm_model, schema_model
from fastapi.responses import JSONResponse
from database_conn import *
orm_model.Base.metadata.create_all(bind=engine)
domain_name = "http://127.0.0.1:8000"
email_password = "password"
email_host = "host.domain.com"
email_address = "username@domain.com"
email_port = 465
some_api_keys = "apikey"


