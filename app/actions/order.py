from sqlmodel import Session, select

from app import actions
from app.models import db as models
from app.models.pydantic.order import OrderItem


class Order:
    MODEL = models.Order

    @classmethod
    async def create(cls, session: Session, order_items: list[OrderItem]) -> MODEL:
        order = models.Order()
        session.add(order)
        for item in order_items:
            product = await actions.Product.read_one(id=item.product_id, session=session)
            order_item = await actions.OrderItem.create(
                product=product, order=order, quantity=item.quantity, session=session
            )
            order.order_items.append(order_item)

        session.commit()
        session.refresh(order)
        return order
