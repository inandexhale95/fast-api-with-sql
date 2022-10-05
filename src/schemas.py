from typing import List

import datetime
import pydantic


class _PostBase(pydantic.BaseModel):
    title: str
    content: str


class PostCreate(_PostBase):
    pass


class Post(_PostBase):
    id: int
    owner_id: int
    date_created: datetime.datetime
    date_last_updated: datetime.datetime

    class Config:
        orm_mode = True


class _UserBase(pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True
