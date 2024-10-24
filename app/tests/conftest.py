import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.db import dispose_db, engine, initialize_db
from app.main import app
from app.models import db as models


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    initialize_db()
    yield
    dispose_db()


@pytest.fixture
def products() -> list[models.Product]:
    products = [models.Product(name=f"Product {n + 1}", price=10) for n in range(5)]
    ingredients = [models.Ingredient(name=f"Ingredient {n + 1}", stock_quantity=2000) for n in range(5)]

    with Session(engine) as session:
        session.add_all(products)
        session.add_all(ingredients)
        session.flush()

        for product, ingredient in zip(products, ingredients):
            session.add(models.ProductIngredient(product_id=product.id, ingredient_id=ingredient.id, quantity=200))
        session.commit()

        return list(session.exec(select(models.Product)).all())


@pytest.fixture
def orders(products):
    order_items = [models.OrderItem(product=product, quantity=1) for product in products]
    orders = [models.Order(order_items=[order_item]) for order_item in order_items]
    with Session(engine) as session:
        session.add_all(orders)
        session.commit()
        return list(session.exec(select(models.Order)).all())
