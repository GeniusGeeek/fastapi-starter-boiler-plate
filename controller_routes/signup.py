from controller_model import signup
from app_utils.master_imports import *
from fastapi import FastAPI
import requests
from enum import Enum







router = APIRouter()




@router.post('/signup',tags=["User Account"])
def register(user: schema_model.User, db: Session = Depends(get_db)):
    create_user = signup.check_email_exist(db, user.email)
    if(create_user):
        #raise HTTPException(status_code=400, detail="Email already registered")
        message= {"message":"Email already registered"}
        return JSONResponse(status_code=400, content=message)
    else:
        return signup.create_user(user, db)
    
    
@router.post('/resend-account-verification',tags=["User Account"])
def resendVerify(email: str, db: Session = Depends(get_db)):
    create_user = signup.check_email_exist(db, email)
    if(create_user):
        return signup.resendVerifyModel(email, db)
    else:
        #raise HTTPException(status_code=400, detail="Email already registered")
        message= {"message":"Email not found"}
        return JSONResponse(status_code=400, content=message)
    
@router.post('/verify-account',tags=["User Account"])
def VerifyAcct(email: str, email_otp:str, db: Session = Depends(get_db)):
    create_user = signup.check_email_exist(db, email)
    if(create_user):
        return signup.VerifyAcctModel(email, int(email_otp), db)
    else:
        #raise HTTPException(status_code=400, detail="Email does not exit")
        message= {"message":"Email does not exit"}
        return JSONResponse(status_code=400, content=message)

@router.post('/gmail-auth-signup/{token_id}', tags=["Account auth"])
def gmail_register(token_id: str, db: Session = Depends(get_db)):
    response = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token="+ token_id)
    res = response.json()
    if(res.get("error") is not None):
      return {"message":"Invalid Id Token"}
    else:
      create_user = signup.check_email_exist(db, res['email'])
      if(create_user):
        #raise HTTPException(status_code=400, detail="Email already registered")
        message= {"message":"Email already registered"}
        return JSONResponse(status_code=400, content=message)
      else:
        class googleUser(str, Enum):
            name = res['name']
            username = res['given_name']
            email = res['email']
        return signup.create_user_from_google_auth(googleUser, db)
       
