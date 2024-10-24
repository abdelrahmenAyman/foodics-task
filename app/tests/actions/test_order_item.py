from datetime import datetime

import pytest
from sqlmodel import select

from app.actions.order_item import OrderItem
from app.models import db as models


@pytest.mark.asyncio
class TestOrderItem:
    async def test_create_order_item(self, session):
        product = models.Product(name="Product 1", price=10)
        order = models.Order()
        await OrderItem.create(session=session, product=product, order=order, quantity=2)

        fetched_order_item = session.exec(select(models.OrderItem).where(models.OrderItem.id == 1)).one()

        assert fetched_order_item.id == 1
        assert fetched_order_item.product == product
        assert fetched_order_item.order == order
