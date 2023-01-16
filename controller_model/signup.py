from sqlalchemy.orm import Session
from models import orm_model, schema_model
from passlib.context import CryptContext
import random
import time


from myutils import app

import smtplib
from email.message import EmailMessage





def create_user(user_details: schema_model.User, db: Session):
    rand_num = random.randint(100000, 999999)
    account_hash_str = str(time.time()) + str(rand_num)
    account_hash = app.generate_account_hash(account_hash_str) #used for password reset 
    receiver_email = user_details.email
    otp_toSend = random.randint(1000,9999)
    generate_unique_id = None
    while True:
        generate_unique_id = random.randint(100000,999999)
        check_unique_id = db.query(orm_model.User).filter(orm_model.User.unique_id == generate_unique_id).first()
        if(check_unique_id):
            generate_unique_id = random.randint(100000,999999)
            check_unique_id = db.query(orm_model.User).filter(orm_model.User.unique_id == generate_unique_id).first()
            if(check_unique_id is None):
                break 
        else:
            break
    add_user = orm_model.User(
        hashed_password=app.hash_password(user_details.password),
        username=user_details.username,
        email=user_details.email,
        name=user_details.name,
        account_hash=account_hash,
        unique_id=generate_unique_id,
        email_otp = otp_toSend


    )
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    #send_mail(receiver_email)
    app.send_mail("mailServer", "sender", "password", receiver_email,"Welcome, Use the following OTP to verify your account, OTP: "+str(otp_toSend), "Welcome to Fast API")
    return {"message":"Registeration successful"}


def sendVerifyModel(email, db):
    def sendVerifyModel(email, db):
    receiver_email = email
    otp_toSend = random.randint(1000,9999)
    data = db.query(orm_model.User).filter(orm_model.User.email == email).first()
    if (data is not None):

        data.email_otp = otp_toSend
        db.commit()
        db.refresh(data)
        app.send_mail("mailServer", "sender", "password", receiver_email,"Hi, Use the following OTP to verify your account, OTP: "+str(otp_toSend), "FAST API Verify Account")
        return {"message": "Verification Code sent successfully"}

    else:
        return {"message": "condition not found"}   
   


def VerifyAcctModel(email, email_otp, db):
    try:
         data = db.query(orm_model.User).filter(orm_model.User.email == email).first()
         if (email_otp == data.email_otp):
             data.account_verified = 1

             db.commit()
             db.refresh(data)
             
             
             
             return {"status":"success","message":"Verified Successfully"}
         else:
            return {"message": "Email and Account verification failed, Wrong OTP"}



     except Exception as e:
        return {"message": "An error occured: "+ str(e)}   


    
def create_user_from_google_auth(user_details, db: Session):
    rand_num = random.randint(100000, 999999)
    account_hash_str = str(time.time()) + str(rand_num)
    account_hash = app.generate_account_hash(account_hash_str) #used for password reset 
    receiver_email = user_details.email
    add_user = orm_model.User(
        username=user_details.username,
        email=user_details.email,
        name=user_details.name,
        account_hash=account_hash
    )
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    #send_mail(receiver_email)
    app.send_mail("mailServer", "sender", "password", receiver_email,"Welcome, Use the following OTP to verify your account, OTP: "+str(otp_toSend), "Welcome to Fast API")
    return {"message":"Registeration successful"}
   


def check_email_exist(db: Session, email: str):
    return db.query(orm_model.User).filter(orm_model.User.email == email).first()


def send_mail(address_to):

  msg = EmailMessage()
  fromaddr = 'email address'
  toaddrs = address_to
  msgtxt = "Message"
  msg.set_content(msgtxt)
  msg['Subject'] = "Subject"
  msg['From'] = fromaddr
  msg['To'] = toaddrs

  try:

     #smtpObj = smtplib.SMTP('localhost') if localohost
     #use smtplib.SMTP() if port is 587
     with smtplib.SMTP_SSL('server', 465) as smtp:
        #server.starttls() if port is 587
         smtp.login("email address", "password")
         smtp.send_message(msg)
         return {"sent mail"}

  #except smtplib.SMTPException:
  except Exception as e:
      return {"message": "Problem Ocuured while sending email, mail not sent!", "error": e}


def reset_password(user: schema_model.resetPassword, db: Session):
    data = db.query(orm_model.User).filter(orm_model.User.email == user.email).first()
    data.hashed_password = app.hash_password(user.new_password)
    db.commit()
    db.refresh(data)
    return {"message": "Password reset successfull"}
