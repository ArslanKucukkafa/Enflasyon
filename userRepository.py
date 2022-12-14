import time
from datetime import datetime, timedelta
from typing import TypeVar, Generic, Optional

from anyio import ExceptionGroup
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from config import SECRET_KEY, ALGORITHM

T = TypeVar('T')


class BaseRepo():

    @staticmethod
    def retrieve_all(db: Session, model: Generic[T]):
        return db.query(model).all()

    @staticmethod
    def retrieve_by_id(db: Session, model: Generic[T], id: int):
        return db.query(model).filter(model.id == id).all()

    @staticmethod
    def insert(db: Session, model: Generic[T]):

        db.add(model)
        db.commit()
        db.refresh(model)

    @staticmethod
    def update(db: Session, model: Generic[T]):
        db.commit()
        db.refresh(model)

    @staticmethod
    def delete(db: Session, model: Generic[T]):
        db.delete(model)
        db.commit()


class UsersRepo(BaseRepo):

    @staticmethod
    def find_by_username(db: Session, model: Generic[T], username: str):
        return db.query(model).filter(model.username == username).first()


class JWTRepo():

    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt

    def decode_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
            return decode_token if decode_token["exp"] >= int(time.time()) else None
        except Exception as error:
            raise ExceptionGroup('there were problems', error)


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication sheme.")
            if  self.verfity_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expiredd token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status=403, detail="Invalid authorization code.")

    def verfity_jwt(Self, jwttoken: str):
        isTokenValid: bool = False

        try:
            payload = JWTRepo.decode_token(jwttoken)
        except Exception:
            isTokenValid = True

        return isTokenValid

    def jwtBreak(self,request: Request):

        ss = "jwtBreak is running"

        credentials: HTTPAuthorizationCredentials =  super(JWTBearer, self).__call__(request)

        payload = jwt.decode(credentials.credentials, SECRET_KEY,ALGORITHM)
        print(payload["sub"],payload["sub1"])

        return ss