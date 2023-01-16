from myutils.master_imports import *
from controller_model import  signin

from fastapi.security import OAuth2PasswordRequestForm
from myutils import app  
import requests



ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 300




router = APIRouter()

@router.post("/signin", summary="user login",tags=["User Account"] )
def login(user_login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  login_user = signin.login_email(user_login_details.username,db)
  #return login_user

   if(app.verify_password(user_login_details.password, login_user.hashed_password)):
      if (login_user.email_otp == 1):
          data = {"sub": login_user.id}
          jwt_exp_time = app.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
          encoded_jwt = app.create_jwt_token(data, jwt_exp_time)
          return {"access_token": encoded_jwt, "message": "login successfull", "user_details": login_user, "token type": "bearer"}
      else:
          return {"message": "Account not verified, verify account to login"}

   else:
      raise HTTPException(status_code=400, detail="wrong password")


  else:  
    raise HTTPException(status_code=400, detail="email does not exist")


@router.post("/gmail_auth_signin", summary="user gmail auth login" )
def gmail_login(token_id: str, db: Session = Depends(get_db)):
  response = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token="+ token_id)
  res = response.json()
  if(res.get("error") is not None):
      return {"message":"Invalid Id Token"}
  else:

   login_user = signin.login_email(res['email'],db)
   #return login_user

   if(login_user):
       data = {"sub": login_user.id}
       jwt_exp_time = app.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
       encoded_jwt = app.create_jwt_token(data, jwt_exp_time)
       return {"access_token": encoded_jwt, "message": "login successfull", "user_details": login_user, "token type": "bearer"}

     
   else:  
     raise HTTPException(status_code=400, detail="email does not exist")


