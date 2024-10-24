from sqlmodel import Session, select

from app import actions
from app.models import db as models


class OrderItem:
    MODEL = models.OrderItem

    @classmethod
    async def create(cls, session: Session, product: models.Product, order: models.Order, quantity: int) -> MODEL:
        instance = cls.MODEL(product=product, order=order, quantity=quantity)
        await actions.Ingredient.update_product_ingredients_stock(
            product=product, product_quantity=quantity, session=session
        )
        session.add(instance)
        session.commit()
        return instance
