from typing import Optional, List
from pydantic import BaseModel, Field

class User(BaseModel):
      email: str = Field(example="foomail@mail.com")
      name: str = Field(example="foo admin")
      username:str = Field(example="foo")
      password:str = Field(example="password")
      referal_code:str = Field(example="122921")
      country:str = Field(example="Nigeria")
      country_code:str = Field(example="+234")
      mobile_number:str = Field(example="90339***09")
      
      
     

class user_login(BaseModel):
      email:str = Field(example="foomail@mail.com")
      password:str = Field(example="password")



class forgotPassword(BaseModel):
      email:str = Field(example="foomail@mail.com")


class resetPassword(BaseModel):
    email: str = Field(example="foomail@mail.com")
    reset_code: int = Field(example="nskdnsdksdn223eee")
    new_password:str = Field(example="newPassword")
      
 
class changePassword(BaseModel):
    new_password: str = Field(example="newPassword")
    unique_id: int = Field(example="111111")


class User_EditProfile(BaseModel):
    name: str = Field(example="richard")
    email: str = Field(example="foo@mail.com")
    username: str = Field(example="adminUser")
    unique_id: int = Field(example="adminUser")
 
      
      
      
      

      
