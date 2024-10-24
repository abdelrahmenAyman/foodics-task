import pytest
from fastapi.testclient import TestClient
from sqlmodel import select

from app.models import db as models


@pytest.mark.asyncio
class TestCreateOrderRoutes:
    url = "/orders/"

    @pytest.fixture(autouse=True)
    def mock_send_email(self, mocker):
        self.mock_email = mocker.patch("app.actions.ingredient.send_email", return_value=1)

    async def test_create_order_products_field_missing(self, client: TestClient):
        data = {}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 422

    async def test_create_order_products_field_empty(self, client):
        data = {"products": []}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 422
        assert "Products field cannot be empty." in response.json()["detail"][0]["msg"]

    async def test_create_order_product_id_is_missing(self, client):
        data = {"products": [{"quantity": 1}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 422

    async def test_create_order_product_id_is_not_integer(self, client):
        data = {"products": [{"product_id": "s", "quantity": 2}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 422

    async def test_create_order_product_quantity_is_missing(self, client):
        data = {"products": [{"product_id": 1}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 422

    async def test_create_order_product_quantity_is_not_integer(self, client):
        data = {"products": [{"product_id": 1, "quantity": "s"}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 422

    async def test_create_order_product_quantity_is_negative(self, client):
        data = {"products": [{"product_id": 1, "quantity": -1}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 422

    async def test_create_order_product_quantity_is_zero(self, client):
        data = {"products": [{"product_id": 1, "quantity": 0}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 422

    async def test_create_order_product_id_does_not_exist(self, client, products):
        data = {"products": [{"product_id": 100, "quantity": 2}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 404

    async def test_create_order_product_ingredients_exceeds_stock_quantity(self, client, products):
        data = {"products": [{"product_id": 1, "quantity": 2000}, {"product_id": 2, "quantity": 20}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 400

    async def test_create_order_success(self, client, session, products):
        data = {"products": [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 1}]}
        response = client.post(url=self.url, json=data)

        assert response.status_code == 201
        result = session.exec(
            select(models.Product, models.ProductIngredient, models.OrderItem)
            .join(models.ProductIngredient)
            .join(models.OrderItem)
            .join(models.Order)
            .where(models.Order.id == response.json()["id"])
        ).all()

        for product, product_ingredient, order_item in result:
            for ingredient in product.ingredients:
                new_stock_quantity = 2000 - order_item.quantity * product_ingredient.quantity
                assert ingredient.stock_quantity == new_stock_quantity
        assert len(session.exec(select(models.Order)).all()) == 1

    async def test_create_order_ingredient_drops_to_fifty_percent(self, client, products, session):
        data = {"products": [{"product_id": 1, "quantity": 5}]}

        response = client.post(url=self.url, json=data)

        assert response.status_code == 201
        assert self.mock_email.call_count == 0
        assert not session.get(models.Ingredient, 1).is_alerted

    async def test_create_order_ingredient_drops_below_fifty_percent(self, client, products, session):
        data = {"products": [{"product_id": 1, "quantity": 6}]}

        response = client.post(url=self.url, json=data)

        assert response.status_code == 201
        assert self.mock_email.call_count == 1
        assert session.get(models.Ingredient, 1).is_alerted

    async def test_create_order_ingredient_stock_drops_below_threshold_twice(self, client, products, session):
        data = {"products": [{"product_id": 1, "quantity": 6}]}
        response_1 = client.post(url=self.url, json=data)

        data["products"][0]["quantity"] = 1
        response_2 = client.post(url=self.url, json=data)

        assert response_1.status_code == 201
        assert response_2.status_code == 201
        assert self.mock_email.call_count == 1
        assert session.get(models.Ingredient, 1).is_alerted

    async def test_create_order_ingredient_stock_higher_than_50_percent(self, client, products, session):
        data = {"products": [{"product_id": 1, "quantity": 2}]}

        response = client.post(url=self.url, json=data)

        assert response.status_code == 201
        assert self.mock_email.call_count == 0
        assert not session.get(models.Ingredient, 1).is_alerted
