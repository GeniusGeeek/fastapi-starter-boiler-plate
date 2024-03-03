from sqlalchemy.orm import Session
from models import orm_model, schema_model
import random
from app_utils import utils


def login_email(email: str, db: Session):
    data = db.query(orm_model.User).filter(
        orm_model.User.email == email).first()
    if (data is not None):
        if (data.account_deactiavted == True):
            return "0"
        else:
            return data
    else:
        return "User does not exit"



def forgotPassModel(email, db:Session):
  receiver_email = email
  data = db.query(orm_model.User).filter(orm_model.User.email == email).first()
  if(data is not None):
     otp_toSend = random.randint(1000, 9999)
     try:
        data = db.query(orm_model.User).filter(orm_model.User.email == email).first()
        data.email_otp = otp_toSend
        db.commit()
        db.refresh(data)
        utils.send_mail("server", "senderAddress", "password", receiver_email,
                      "Hi, Use the following OTP to reset your account password, OTP: "+str(otp_toSend), "Reset Account password")
        return {"message": "Reset Code sent successfully"}

     except Exception as e:
        return {"message": "An error occured: "+ str(e)}   
  else:
      return {"message": "email does not exit"}

