from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    token: str
    uid: int


class TokenPayload(BaseModel):
    sub: int = None
