from pydantic import BaseModel,EmailStr
from datetime import datetime,date
from typing import Optional

class Email(BaseModel):
    email : EmailStr

class Create_Account(BaseModel):
    first_name : str
    last_name : str
    password : str
    date_of_birth : date
    phone_number  : str

class UserOut(BaseModel):
    id : int    
    first_name : str
    last_name : str
    created_on : datetime
    date_of_birth : date
    phone_number  : str
    class Config:
        orm_mode = True

class UserDetails(BaseModel):
    bio: str
    image_url: str
    gender: str
    address: str
    updated_on : Optional[datetime]

class Edit(BaseModel):
    first_name : str = None
    last_name : str = None
    created_on : datetime = None
    date_of_birth : date = None
    phone_number  : str = None
    bio: str = None
    image_url: str = None
    gender: str = None
    address: str = None
    

class SetPassword(BaseModel):
    password : str

class ChangePassword(SetPassword):
    new_password : str

class Token(BaseModel):
    access_token : str
    token_type: str
    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id : Optional[str] = None
    class Config:
        orm_mode = True