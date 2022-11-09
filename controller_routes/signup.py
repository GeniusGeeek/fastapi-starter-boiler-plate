from controller_model import signup
from myutils.master_imports import *
from fastapi import FastAPI
import requests
from enum import Enum







router = APIRouter()




@router.post('/signup',tags=["Account auth"])
def register(user: schema_model.User, db: Session = Depends(get_db)):
    create_user = signup.check_email_exist(db, user.email)
    if(create_user):
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        return signup.create_user(user, db)

@router.post('/gmail_auth_signup/{token_id}', tags=["Account auth"])
def gmail_register(token_id: str, db: Session = Depends(get_db)):
    response = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token="+ token_id)
    res = response.json()
    if(res.get("error") is not None):
      return {"message":"Invalid Id Token"}
    else:
      create_user = signup.check_email_exist(db, res['email'])
      if(create_user):
        raise HTTPException(status_code=400, detail="Email already registered")
      else:
        class googleUser(str, Enum):
            name = res['name']
            username = res['given_name']
            email = res['email']
        return signup.create_user_from_google_auth(googleUser, db)
       
