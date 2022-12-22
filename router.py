from fastapi import APIRouter, Depends
from schema import RequestSchema, ResponseSchema, TokenResponse,CartSchema
from sqlalchemy.orm import Session
from config import get_db
from passlib.context import CryptContext
from userRepository import JWTRepo, JWTBearer, UsersRepo
from model import Users
from productModel import Product
import requests
from bs4 import BeautifulSoup
from productRepository import BaseRepo
from cartRepository import CartRepo
import logging

router = APIRouter()

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
    Authentication Router

"""


@router.post('/signup')
async def signup(request: RequestSchema, db: Session = Depends(get_db)):
    try:
        # insert user to db
        #Mevcut kullancı eklenebilir

        #//////-------------/////
        _user = Users(username=request.parameter.data["username"],
                      email=request.parameter.data["email"],
                      password=pwd_context.hash(
                          request.parameter.data["password"]))
        UsersRepo.insert(db, _user)
        return ResponseSchema(code="200", status="Ok", message="Success save data").dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(code="500", status="Error", message="Internal Server Error").dict(exclude_none=True)


@router.post('/login')
async def login(request: RequestSchema, db: Session = Depends(get_db)):
    try:
       # find user by username
        _user = UsersRepo.find_by_username(
            db, Users, request.parameter.data["username"])

        if not pwd_context.verify(request.parameter.data["password"], _user.password):
            return ResponseSchema(code="400", status="Bad Request", message="Invalid password").dict(exclude_none=True)

        token = JWTRepo.generate_token({"sub": _user.username,"sub2":_user.password,"sub3":_user.id})
        return ResponseSchema(code="200", status="OK", message="success login!", result=TokenResponse(access_token=token, token_type="Bearer")).dict(exclude_none=True)
    except Exception as error:

        error_message = str(error.args)
        print(error_message,"Error is occouring")
        logging.error("Error is occouring  3fr4rgtgt4g4")
        return ResponseSchema(code="500", status="Internal Server Error", message="Internal Server Error3333").dict(exclude_none=True)

"""
    Users Router

"""

@router.get("/ProductUpdate")
def ProductUpdate(db: Session = Depends(get_db)):
    r = requests.get("https://www.a101.com.tr/aldin-aldin/?sorter=-price&category_ids=2")
    r.content
    soup = BeautifulSoup(r.content, "html.parser")
    urunIsimleri = soup.find_all("hgroup")
    urunIsimleriTablo = list()
    urunFiyatlariTablo = list()
    for i in urunIsimleri:
        urunIsimleriTablo.append(i.text.replace("\n", "").strip())
    urunfiyarlari = soup.find_all("section", {"class": "prices"})
    for i in urunfiyarlari:
        fiyattext = (i.text.replace("\n", "").replace("₺", " ").replace(",", ".").strip()).rsplit(" ")
        fiyat = float(fiyattext[len(fiyattext) - 1])
        urunFiyatlariTablo.append(fiyat)
    c = 0
    while (c < len(urunIsimleriTablo)):
        # print(urunFiyatlariTablo[c])
        model = Product(productName=urunIsimleriTablo[c], productPrice=urunFiyatlariTablo[c])
        BaseRepo.insert(db, model)
        c += 1



@router.get("/products", dependencies=[Depends(JWTBearer())])
async def retrieve_all(db: Session = Depends(get_db)):

    _products = UsersRepo.retrieve_all(db, Product)
    return ResponseSchema(code="200", status="Ok", message="Sucess retrieve data", result=_products).dict(exclude_none=True)


#@router.post("/sepet",dependencies=[Depends(JWTBearer())])
#async def add_basket(db: Session = Depends(get_db)):

@router.post("/breakingToken")
async def breaking(request:RequestSchema):
     return JWTBearer.jwtBreak(request.parameter.data["token"])


@router.get("/users", dependencies=[Depends(JWTBearer())])
async def retrieve_all(db: Session = Depends(get_db)):
    _user = UsersRepo.retrieve_all(db, Users)
    return ResponseSchema(code="200", status="Ok", message="Sucess retrieve data", result=_user).dict(exclude_none=True)


@router.post("/saveShopingCart",dependencies=[Depends(JWTBearer)])
async def saveShopingCart(request:CartSchema,db:Session = Depends(get_db)):
    a=CartRepo.insert()
    print(request.parameter.data)