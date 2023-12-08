import smtplib
from email.message import EmailMessage
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status, UploadFile, File
# from jose import jwt, JWTError
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import hashlib
from sqlalchemy.orm import Session
from models import orm_model, schema_model
import random
import os
from typing import List
import string
import time
from fastapi.responses import JSONResponse


outh2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str):
    return password_context.verify(password, hashed_password)


def hash_password(password: str):
    return password_context.hash(password)


ACCESS_JWT_EXPIRE_MINUTES = 60 * 24 * 365
ALGORITHM = 'HS256'
SECRET_KEY = "6b6b5e8482ab8253a4d47993cca66cb2710c59b278287917f9ca8f08e2d95ac9"


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    data_to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_JWT_EXPIRE_MINUTES)
    data_to_encode.update({'exp': expires})
    encoded_jwt_data = jwt.encode(
        data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt_data

# def upload_file(file:bytes=File(...)):


def upload_file(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return {"message": "file not a valid type for upload, valid type is image"}
    # if (len(file) > 2000000):
        # return {"message":"file is too large, limit is  1mb"}

    try:
        file_contents = file.file.read()
        destination_path = "uploads/"
        filename = file.filename.split(".")[0]
        filenameExtention = file.filename.split(".").pop()
        modifiedfilename = filename + \
            str(random.randint(100000, 999999))+"."+filenameExtention
        with open(destination_path+modifiedfilename, 'wb') as buffer:
            buffer.write(file_contents)
            if (os.path.getsize(destination_path+modifiedfilename) > 2000000):
                os.remove(destination_path+modifiedfilename)
                return {"message": "file size is large, max size is 2mb"}

            else:
                return {"message": "success", "file_path": destination_path+modifiedfilename}

    except Exception as e:
        return {"message": e}

    finally:
        file.file.close()


def optional_upload_file(file:  Optional[UploadFile] = None):
    try:
        if (file is not None):
            file_contents = file.file.read()
            destination_path = "uploads/"
            filename = file.filename.split(".")[0]
            filenameExtention = file.filename.split(".").pop()
            modifiedfilename = filename + \
                str(random.randint(100000, 999999))+"."+filenameExtention
            modifiedfilenameWithDir = destination_path+modifiedfilename
            with open(destination_path+modifiedfilename, 'wb') as buffer:
                buffer.write(file_contents)
                return {"message": "success", "file_path": modifiedfilenameWithDir}
        else:
                return {"message": "no file to upload"}
    except Exception as e:
        return {"message": e}


async def upload_multiple_files(files: List[UploadFile] = File(...)):
    try:
        uploaded_files = []
        for file in files:
            if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
                return {"message": f"{file.filename} is not a valid type for upload, valid types are image/jpeg, image/png, image/jpg"}

            file_contents = file.file.read()
            destination_path = "uploads/"
            filename = file.filename.split(".")[0]
            filenameExtention = file.filename.split(".").pop()
            modifiedfilename = filename + \
                str(random.randint(100000, 999999))+"."+filenameExtention
            with open(destination_path+modifiedfilename, 'wb') as buffer:
                buffer.write(file_contents)
                if (os.path.getsize(destination_path+modifiedfilename) > 2000000):
                    os.remove(destination_path+modifiedfilename)
                    return {"message": f"{file.filename} is too large, max size is 2mb"}

                else:
                    uploaded_files.append(destination_path+modifiedfilename)

        return {"message": "success", "file_paths": uploaded_files}

    except Exception as e:
        return {"message": e}

    finally:
        for file in files:
            file.file.close()


def auth_user_request(token: str = Depends(outh2_scheme)):
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        decoded_jwt = payload

    # except JWTError as error:
        # return error
    except:
        #raise credentials_exception
        message= {"message":"Could not validate credentials"}
        return JSONResponse(status_code=400, content=message)

    return decoded_jwt


def send_mail(server, sender, password, receipient, message, subject):

    msg = EmailMessage()
    fromaddr = sender
    toaddrs = receipient
    msg = "This is a test email with HTML formatting."
    msg = message
    msgtxt = """<html><body><h1>Hello World!</h1><p>{message}</p></body></html>"""
    msgtxt = msgtxt.format(message=message)
    msg.set_content(msgtxt, subtype='html')
    # msg.add_alternative(message_text, subtype='plain')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    try:

        # smtpObj = smtplib.SMTP('localhost') if localohost
        # use smtplib.SMTP() if port is 587
        with smtplib.SMTP_SSL(server, 465) as smtp:
            # smtp.starttls() if port is 587
            smtp.login(fromaddr, password)
            smtp.send_message(msg)
            return {"message": "sent mail"}

    # except smtplib.SMTPException:
    except Exception as e:
        return {"message": "Problem Ocuured while sending email, mail not sent!", "error": e}


def generate_account_hash(unique_Str):
    result = hashlib.md5(unique_Str.encode())
    return result.hexdigest()


def getUserDetails(userId: str, detail: str, db: Session):
    data = db.query(orm_model.User).filter(
        (orm_model.User.id == userId) | (orm_model.User.unique_id == userId)).first()
    if (data is None):

        #raise HTTPException(status_code=401, detail="USER ID NOT FOUND")
        message= {"message":"USER ID NOT FOUND"}
        return JSONResponse(status_code=400, content=message)
    else:
        return getattr(data, detail)


def generate_unique_random_id():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    pick_chars = ''.join(random.choice(chars) for _ in range(6))
    unique_id = pick_chars+str(int(time.time()))
    return unique_id
