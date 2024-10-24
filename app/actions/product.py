from sqlmodel import Session, select

from app.models import db as models


class Product:
    MODEL = models.Product

    @classmethod
    async def create(cls, session: Session, **kwargs) -> MODEL:
        instance = cls.MODEL(**kwargs)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    async def read_one(cls, session: Session, id: int) -> MODEL:
        statement = select(cls.MODEL).where(cls.MODEL.id == id)
        return session.exec(statement).one()
