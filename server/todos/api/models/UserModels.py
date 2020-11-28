from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class User(BaseModel):
    username: str = Query(None, min_length=4, max_length=15)


class UserAuth(User):
    password: Optional[str] = Query(None, min_length=6, max_length=64)


class UserFunc(User):
    token: Optional[str] = Query(None, min_length=64, max_length=64)
