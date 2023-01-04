from typing import Generic, Optional, TypeVar, Dict
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None


class para(BaseModel):
    data: dict[float, float, float, str, float, float] = None


class RequestSchema(BaseModel):
    parameter: Parameter = Field(...)


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class CartSchema(BaseModel):
    token :str
    earnings:str
    parameter: para = Field(...)
