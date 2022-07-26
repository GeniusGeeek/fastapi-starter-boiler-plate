from myutils.master_imports import *
from controller_model import  signin
from myutils import app  
import random






router = APIRouter()


@router.post("/forget_password", summary="user forget password", tags=["User Account"])
def post_data(post_data_in: schema_model.forgotPassword, db: Session = Depends(get_db)):
  check_email = signin.login_email(post_data_in.email, db)
  #reset_code = check_email.account_hash
  reset_code = check_email.email_otp

  if(check_email):
    signin.forgotPassModel(post_data_in.email, db)
    if(app.send_mail("mailserver", "sender address", "sender password", post_data_in.email, "Hi this is your reset code: "+reset_code, "Subject: Reset Code") == "sent mail"):
      return {"message": "Reset link successfull sent to your email"}

    else:
      
      raise HTTPException(status_code=400, detail="Somthing went  wrong in sending reset code")

  else:  
    raise HTTPException(status_code=400, detail="email does not exist")
