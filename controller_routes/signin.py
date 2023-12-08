from app_utils.master_imports import *
from controller_model import  signin

from fastapi.security import OAuth2PasswordRequestForm
from app_utils import utils  
import requests



ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 300




router = APIRouter()

@router.post("/signin", summary="user login",tags=["User Account"] )
def login(user_login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  login_user = signin.login_email(user_login_details.username,db)
  #return login_user

  if (login_user):
        if (login_user == "0"):

            #raise HTTPException(status_code=400, detail="Account Deactivated")
            message= {"message":"Account Deactivated"}
            return JSONResponse(status_code=400, content=message)

        elif (login_user == "User does not exit"):
            #raise HTTPException(status_code=400, detail="User does not exit")
            message= {"message":"User does not exit"}
            return JSONResponse(status_code=400, content=message)

        else:
            if (utils.verify_password(user_login_details.password, login_user.hashed_password)):
                data = {"sub": login_user.id}
                jwt_exp_time = utils.timedelta(
                    minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                encoded_jwt = utils.create_jwt_token(data, jwt_exp_time)
                return {"access_token": encoded_jwt, "message": "login successfull", "user_details": login_user, "token type": "bearer"}

            else:
                #raise HTTPException(status_code=400, detail="wrong password")
                message= {"message":"wrong password"}
                return JSONResponse(status_code=400, content=message)

  else:
        #raise HTTPException(status_code=400, detail="email does not exist")
        message= {"message":"email does not exist"}
        return JSONResponse(status_code=400, content=message)



@router.post("/gmail-auth-signin", summary="user gmail auth login" )
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
       jwt_exp_time = utils.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
       encoded_jwt = utils.create_jwt_token(data, jwt_exp_time)
       return {"access_token": encoded_jwt, "message": "login successfull", "user_details": login_user, "token type": "bearer"}

     
   else:  
     #raise HTTPException(status_code=400, detail="email does not exist")
     message= {"message":"email does not exist"}
     return JSONResponse(status_code=400, content=message)


