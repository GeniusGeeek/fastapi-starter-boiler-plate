from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import orm_model, schema_model
from database_conn import *
orm_model.Base.metadata.create_all(bind=engine)

