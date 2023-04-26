from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, EmailStr, Field, validator


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    username: str = Field(..., min_length=4, max_length=50, regex="^[a-zA-Z0-9_-]+$",
                          description="The username of the user. It should only contain alphanumeric characters, underscores and hyphens.")

class UserExtended(UserBase):  
    email: EmailStr = Field(..., description="The email address of the user.")
    name: str = Field(..., min_length=4, max_length=100,
                      description="The name of the user.")

class UserCreatePassword(UserExtended):
    password: str = Field(..., min_length=8, max_length=100, regex="^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$",
                          description="The password of the user. It should be at least 8 characters long and contain at least one uppercase letter, one number, and one special character.")
    confirm_password: str = Field(..., min_length=8, max_length=100, regex="^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$",
                          description="Must be same to written password.")

    @validator('confirm_password', allow_reuse = True)
    def passwords_are_same(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError("passwords don't match")
        return v                                   

class UserCreateFull(UserExtended):
    password: str
    subscription_datetime: datetime
    last_active_datetime: datetime

class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=100,
                          description="The password of the user. It should be at least 8 characters long and contain at least one uppercase letter, one number, and one special character.")
    
class UserLoginResponse(UserLogin):
    id: int
    email: EmailStr = Field(..., description="The email address of the user.")
    name: str = Field(..., min_length=1, max_length=100,
                      description="The name of the user.")
    last_active_datetime: datetime


class UserGroupJoin(BaseModel):
    group_id: int
    username: str

class UserGroupCreate(BaseModel):
    name: str
    description: str


class UserGroup(UserGroupCreate):
    id: int
    # members: List[UserExtended] = []
    # messages: List[Message] = []
    class Config:
        orm_mode = True
        
class User(UserExtended):
    id: int
    is_active: bool
    subscription_datetime: datetime
    last_active_datetime: datetime
    items: List[Item] = []
    groups: List[UserGroup] = []

    class Config:
        orm_mode = True



class MessageCreate(BaseModel):
    text: str
    sender_username: str

class Message(MessageCreate):
    id: int
    group: UserGroup
    sender: User
       
    timestamp: datetime

    class Config:
        orm_mode = True