from typing import Generic, TypeVar
from sqlalchemy.orm import Session



T = TypeVar('T')


class BaseRepo():

    @staticmethod
    def retrieve_all(db: Session, productModel: Generic[T]):
        return db.query(productModel).all()

    @staticmethod
    def retrieve_by_id(db: Session, productModel: Generic[T], id: int):
        return db.query(productModel).filter(productModel.id == id).all()

    @staticmethod
    def insert(db: Session, productModel: Generic[T]):
        db.add(productModel)
        db.commit()
        db.refresh(productModel)

    @staticmethod
    def update(db: Session, productModel: Generic[T]):
        db.commit()
        db.refresh(productModel)

    @staticmethod
    def delete(db: Session, productModel: Generic[T]):
        db.delete(productModel)
        db.commit()
