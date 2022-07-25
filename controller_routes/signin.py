# from fastapi import Depends, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from models import orm_model,schema_model
# from controller_model import signin
# from database_conn import *
# orm_model.Base.metadata.create_all(bind=engine)
from myutils.master_imports import *
from controller_model import  signin

from fastapi.security import OAuth2PasswordRequestForm
from myutils import app  


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 300




router = APIRouter()

@router.post("/signin", summary="user login" )
def login(user_login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  login_user = signin.login_email(user_login_details.username,db)
  #return login_user

  if(login_user):
    if(app.verify_password(user_login_details.password, login_user.hashed_password)):
      data = {"sub": login_user.id}
      jwt_exp_time = app.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      encoded_jwt = app.create_jwt_token(data, jwt_exp_time)
      return {"access_token": encoded_jwt, "message": "login successfull", "user_details": login_user, "token type": "bearer"}

    else:
      raise HTTPException(status_code=400, detail="wrong password")

  else:  
    raise HTTPException(status_code=400, detail="email does not exist")
