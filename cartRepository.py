from typing import Generic, TypeVar
from sqlalchemy.orm import Session



T = TypeVar('T')


class CartRepo():

    @staticmethod
    def retrieve_all(db: Session, productCartModel: Generic[T]):
        return db.query(productCartModel).all()

    @staticmethod
    def retrieve_by_id(db: Session, productCartModel: Generic[T], id: int):
        return db.query(productCartModel).filter(productCartModel.id == id).all()

    @staticmethod
    def insert(db: Session, productCartModel: Generic[T]):
        db.add(productCartModel)
        db.commit()
        db.refresh(productCartModel)

    @staticmethod
    def update(db: Session, productCartModel: Generic[T]):
        db.commit()
        db.refresh(productCartModel)

    @staticmethod
    def delete(db: Session, productCartModel: Generic[T]):
        db.delete(productCartModel)
        db.commit()
