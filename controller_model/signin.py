from sqlalchemy.orm import Session
from models import orm_model, schema_model
import random
from myutils import app

def login_email(email: str,db: Session):
  return db.query(orm_model.User).filter(orm_model.User.email == email).first()


def forgotPassModel(email, db:Session):
  receiver_email = email
  otp_toSend = random.randint(1000, 9999)
  try:
        data = db.query(orm_model.User).filter(orm_model.User.email == email).first()
        data.email_otp = otp_toSend
        db.commit()
        db.refresh(data)
            
           


  except Exception as e:
        return {"message": "An error occured: "+ str(e)}   

  app.send_mail("mailServer", "sender", "password", receiver_email,"Hi, Use the following OTP to reset your account password, OTP: "+str(otp_toSend), "FAST API reset Account")
  return {"message": "Reset Code sent successfully"}

