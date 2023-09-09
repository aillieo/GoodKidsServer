from typing import List
from fastapi import status, Depends, HTTPException
from pydantic import ValidationError
from database import Base, engine, SessionLocal
from fastapi.security import OAuth2PasswordBearer
import models
import schemas
from jose import jwt
import security
from sqlalchemy.orm import Session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(token: str = Depends(reusable_oauth2), session: Session = Depends(get_session)) -> schemas.User:
    print(token)
    try:
        payload = jwt.decode(
            token, security.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        print(payload)

        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = session.query(models.User).get(token_data.sub)

    # check if user item with given id exists. If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(
            status_code=404, detail=f"user item with id {id} not found")

    return user
