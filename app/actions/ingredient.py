from sqlmodel import Session

from app import actions
from app.errors import IngredientStockNotEnough
from app.models import db as models
from app.utils.send_email import send_email


class Ingredient:
    @classmethod
    async def update_product_ingredients_stock(cls, product: models.Product, product_quantity: int, session: Session):
        for ingredient in product.ingredients:
            await cls._update_stock(
                ingredient=ingredient, product=product, session=session, product_quantity=product_quantity
            )
            await cls._check_stock_and_alert(ingredient)

    @classmethod
    async def _update_stock(
        cls, ingredient: models.Ingredient, product: models.Product, product_quantity: int, session: Session
    ):
        product_ingredient = await actions.ProductIngredient.read_one(
            product=product, ingredient=ingredient, session=session
        )
        ingredient.stock_quantity -= product_quantity * product_ingredient.quantity
        if ingredient.stock_quantity < 0:
            session.rollback()
            raise IngredientStockNotEnough(f"Not enough stock for product {product.name}")

    @classmethod
    async def _check_stock_and_alert(cls, ingredient: models.Ingredient):
        if ingredient.stock_quantity < ingredient.threshold and not ingredient.is_alerted:
            ingredient.is_alerted = True
            await send_email(ingredient)
