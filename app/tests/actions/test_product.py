import pytest
from sqlmodel import select

from app.actions.product import Product
from app.models import db as models


@pytest.mark.asyncio
class TestProduct:
    async def test_create_product(self, session):
        product = await Product.create(session=session, name="Test Product", price=10)
        fetched_product = session.exec(select(models.Product).where(models.Product.id == 1)).one()

        assert fetched_product.id == 1

    async def test_read_product(self, session):
        product = models.Product(name="Test Product", price=12)
        session.add(product)
        session.commit()

        fetched_ingredient = await Product.read_one(id=1, session=session)

        assert fetched_ingredient.ingredients == []
        assert fetched_ingredient.id == 1
        assert fetched_ingredient.name == "Test Product"
