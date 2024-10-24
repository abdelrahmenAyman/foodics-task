from sqlmodel import Session, select

from app.models import db as models


class ProductIngredient:
    @classmethod
    async def read_one(cls, product: models.Product, ingredient: models.Ingredient, session: Session):
        return session.exec(
            (
                select(models.ProductIngredient)
                .where(models.ProductIngredient.product_id == product.id)
                .where(models.ProductIngredient.ingredient_id == ingredient.id)
            )
        ).one()
