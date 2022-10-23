import smtplib
from email.message import EmailMessage
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
#from jose import jwt, JWTError
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import  OAuth2PasswordBearer
import hashlib

outh2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str):
    return password_context.verify(password, hashed_password)


def hash_password(password: str):
    return password_context.hash(password)


ACCESS_JWT_EXPIRE_MINUTES = 60 * 24 * 365
ALGORITHM = 'HS256'
SECRET_KEY = "6b6b5e8482ab8253a4d47993cca66cb2710c59b278287917f9ca8f08e2d95ac9"

def create_jwt_token(data: dict, expires_delta: Optional[timedelta]= None):
    data_to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_JWT_EXPIRE_MINUTES)
    data_to_encode.update({'exp': expires})
    encoded_jwt_data = jwt.encode(data_to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt_data

def upload_file(file:UploadFile):
    try:
        file_contents = file.file.read()
        destination_path = "uploads/"
        with open(destination_path+file.filename, 'wb') as buffer:
            buffer.write(file_contents)
            return {"message":"success","file_path":destination_path+file.filename}

    except Exception as e:
        return {"message":e}
     
    finally:
        file.file.close()


def auth_user_request(token: str = Depends(outh2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        decoded_jwt = payload

    #except JWTError as error:
        #return error
    except:
        raise credentials_exception

    return decoded_jwt


def send_mail(server,sender,password,receipient,message, subject):

  msg = EmailMessage()
  fromaddr = sender
  toaddrs = receipient
  msgtxt = message
  msg.set_content(msgtxt)
  msg['Subject'] = subject
  msg['From'] = fromaddr
  msg['To'] = toaddrs

  try:

     #smtpObj = smtplib.SMTP('localhost') if localohost
     #use smtplib.SMTP() if port is 587
     with smtplib.SMTP_SSL(server, 465) as smtp:
        #server.starttls() if port is 587
         smtp.login(fromaddr, password)
         smtp.send_message(msg)
         return "sent mail"

  #except smtplib.SMTPException:
  except Exception as e:
      return {"message": "Problem Ocuured while sending email, mail not sent!", "error": e}




def generate_account_hash(unique_Str):
    result = hashlib.md5(unique_Str.encode())
    return result.hexdigest()
