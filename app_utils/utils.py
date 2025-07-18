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

import mimetypes
from pathlib import Path
import re


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
        return {"message": str(e)}

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
        # raise credentials_exception
        message = {"message": "Could not validate credentials"}
        return JSONResponse(status_code=400, content=message)

    return decoded_jwt


def send_mail(server, sender, password, recipients_string, message, subject, email_port, attachments: list[str | tuple[str, bytes]] | None = None):
    # recipients_string can be in this format address1@gmail.com or address1@gmail.com,address2@gmail.com...addressN@gmail.com
    recipients = [email.strip()
                  for email in recipients_string.split(',')]  # Convert to list

    try:

        # smtpObj = smtplib.SMTP('localhost') if localohost
        # use smtplib.SMTP() if port is 587
        with smtplib.SMTP_SSL(server, 465) as smtp:
            # smtp.starttls() if port is 587
            fromaddr = sender
            smtp.login(fromaddr, password)

            for recipient in recipients:
                msg = EmailMessage()

                toaddrs = recipient
                msgtxt = """<html><body><p>Good day dear,</p><p>{message}</p></body></html>"""
                msgtxt = msgtxt.format(message=message)
                msg.set_content(msgtxt, subtype='html')
                # msg.add_alternative(message_text, subtype='plain')
                msg['Subject'] = subject
                msg['From'] = fromaddr
                msg['To'] = toaddrs

                # ‑‑‑ Attach files (if any) ‑‑‑
                if attachments:
                    for item in attachments:
                        if isinstance(item, tuple):
                            #   (filename, bytes) form
                            filename, data = item
                            maintype, subtype = "application", "octet-stream"
                        else:
                            #   path‑string form
                            path = Path(item)
                            filename = path.name
                            data = path.read_bytes()
                            # guess mime‑type
                            maintype, subtype = mimetypes.guess_type(filename)[
                                0].split('/')

                        msg.add_attachment(
                            data,
                            maintype=maintype,
                            subtype=subtype,
                            filename=filename
                        )

                smtp.send_message(msg)
        return {"message": "sent mails"}

    # except smtplib.SMTPException:
    except Exception as e:
        import traceback
        return {"message": "Problem Ocuured while sending email, mail not sent!", "error": str(e), "trace": traceback.format_exc()}


def generate_account_hash(unique_Str):
    result = hashlib.md5(unique_Str.encode())
    return result.hexdigest()


def getUserDetails(userId: str, detail: str, db: Session):
    data = db.query(orm_model.User).filter(
        (orm_model.User.id == userId) | (orm_model.User.unique_id == userId)).first()
    if (data is None):

        raise HTTPException(status_code=401, detail="USER ID NOT FOUND")

    else:
        return getattr(data, detail)


def getTableDetailsByTableClassName(table_class_name, details, id: str, db: Session):
    # Dynamically get the class from the module
    table_class = getattr(orm_model, table_class_name)

    data = db.query(table_class).filter(
        table_class.id == id).first()
    if (data is None):

        raise HTTPException(
            status_code=401, detail="ID NOT FOUND")

    else:
        return getattr(data, details)


def convert_datestring_to_standard_format(date_string):
    # ALWAYS USE THIS TO FORMAT DATESTRING TO BE SAVED TO DATABASE OR DATESTRING TO QUERY/COMPARE AGAINST DATESTRING IN DATABASE FOR COMPATILIBILITY ISSUES
    # it will return the standard format based on the input some standard format are: YYYY-MM-DD HH:MM:SS YYYY-MM-DD
    # Remove invalid characters using a regular expression (allow only digits, slashes, and hyphens)
    if re.search(r'[^0-9/\- ]', date_string):
        raise HTTPException(
            status_code=401, detail="Date format not recognized")

    # Try different common formats
    possible_formats = [
        ("%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%d/%m/%Y", "%Y-%m-%d"),
        ("%d-%m-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%d-%m-%Y", "%Y-%m-%d"),
        ("%m/%Y/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%m/%Y/%d", "%Y-%m-%d"),
        ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%Y-%m-%d", "%Y-%m-%d"),
        ("%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%Y/%m/%d", "%Y-%m-%d"),
        ("%d/%Y/%m %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%d/%Y/%m", "%Y-%m-%d"),
        # US-style (MM/DD/YYYY with time)
        ("%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%m/%d/%Y", "%Y-%m-%d"),                     # US-style (MM/DD/YYYY)
        ("%d-%Y-%m %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%d-%Y-%m", "%Y-%m-%d"),
        ("%d/%m/%Y %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f"),  # Include milliseconds
        ("%d-%m-%Y %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f"),
        ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f"),
    ]

    # Try to parse with each format
    for input_format, output_format in possible_formats:
        try:
            date_obj = datetime.strptime(date_string, input_format)
            return date_obj.strftime(output_format)
        except ValueError:
            continue  # Try the next format if this one doesn't work

    # If no formats match, raise an error
    raise HTTPException(status_code=401, detail="Date format not recognized")


def generate_unique_random_id():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    pick_chars = ''.join(random.choice(chars) for _ in range(6))
    unique_id = pick_chars+str(int(time.time()))
    return unique_id
