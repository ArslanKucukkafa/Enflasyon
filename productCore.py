from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup
from config import get_db
from productRepository import BaseRepo
from productModel import Product


class scraping():

  def __init__(self):
        print("product scraping is starting")


  def productUpdate(self,db: Session = Depends(get_db)):

        r= requests.get("https://www.a101.com.tr/aldin-aldin/?sorter=-price&category_ids=2")
        r.content
        soup = BeautifulSoup(r.content,"html.parser")
        urunIsimleri= soup.find_all("hgroup")
        urunIsimleriTablo=list()
        urunFiyatlariTablo=list()
        for i in urunIsimleri:
             urunIsimleriTablo.append(i.text.replace("\n","").strip())
        urunfiyarlari =  soup.find_all("section",{"class":"prices"})
        for i in urunfiyarlari:
              fiyattext=(i.text.replace("\n","").replace("₺"," ") .replace(",",".").strip()).rsplit(" ")
              fiyat = float(fiyattext[len(fiyattext)-1])
              urunFiyatlariTablo.append(fiyat)
        c = 0
        while (c < len(urunIsimleriTablo)):
            #print(urunFiyatlariTablo[c])
            model = Product(productName=urunIsimleriTablo[c], productPrice=urunFiyatlariTablo[c])
            BaseRepo.insert(db, model)
            c += 1
