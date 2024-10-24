from datetime import datetime

import pytest
from sqlmodel import select

from app.actions.order import Order
from app.models import db as models
from app.models import pydantic as schemas


@pytest.mark.asyncio
class TestOrder:
    async def test_create_order_with_order_items(self, session, products):
        order_item_1 = schemas.OrderItem(product_id=1, quantity=2)
        order_item_2 = schemas.OrderItem(product_id=2, quantity=1)

        order = await Order.create(session=session, order_items=[order_item_1, order_item_2])
        fetched_order = session.exec(select(models.Order).where(models.Order.id == 1)).one()

        assert fetched_order.id == 1
        assert len(fetched_order.order_items) == 2
