from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
      email: str
      name: str
      username:str 
      password:str 
      
     

class user_login(BaseModel):
      email:str
      password:str



class forgotPassword(BaseModel):
      email:str


class resetPassword(BaseModel):
    email: str
    reset_code: str
    new_password:str

      
