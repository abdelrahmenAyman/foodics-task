import pytest

from app.actions.ingredient import Ingredient
from app.errors import IngredientStockNotEnough
from app.models import db as models


@pytest.mark.asyncio
class TestIngredient:
    @pytest.fixture(autouse=True)
    def mock_send_email(self, mocker):
        self.mock_email = mocker.patch("app.actions.ingredient.send_email", return_value=1)

    @pytest.fixture
    def ingredient(self, session):
        ingredient = models.Ingredient(name="Test Ingredient", stock_quantity=100)
        session.add(ingredient)
        session.commit()
        return ingredient

    async def test_ingredient_stock_quantity_less_than_50(self, ingredient):
        ingredient.stock_quantity = 49
        await Ingredient._check_stock_and_alert(ingredient)
        assert ingredient.is_alerted
        assert self.mock_email.call_count == 1

    async def test_ingredient_stock_quantity_equal_to_50(self, ingredient):
        ingredient.stock_quantity = 50
        await Ingredient._check_stock_and_alert(ingredient)
        assert not ingredient.is_alerted
        assert self.mock_email.call_count == 0

    async def test_ingredient_stock_quantity_greater_than_50(self, ingredient):
        ingredient.stock_quantity = 51
        await Ingredient._check_stock_and_alert(ingredient)
        assert not ingredient.is_alerted
        assert self.mock_email.call_count == 0

    async def test_update_ingredient_stock_less_than_zero(self, products, session):
        product = products[0]
        session.add(product)
        old_stock = product.ingredients[0].stock_quantity
        with pytest.raises(IngredientStockNotEnough):
            await Ingredient._update_stock(
                ingredient=product.ingredients[0], product=product, session=session, product_quantity=21
            )
        assert product.ingredients[0].stock_quantity == old_stock

    async def test_update_ingredient_stock_quantity(self, products, session):
        product = products[0]
        session.add(product)
        old_stock = product.ingredients[0].stock_quantity
        session.add(product)
        await Ingredient._update_stock(
            ingredient=product.ingredients[0], product=product, session=session, product_quantity=2
        )
        assert product.ingredients[0].stock_quantity == old_stock - 2 * 200
