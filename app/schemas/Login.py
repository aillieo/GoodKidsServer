# generated by datamodel-codegen:
#   filename:  Login.json

from __future__ import annotations

from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str
