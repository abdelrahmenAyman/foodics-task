from sqlmodel import Session

from app.db import engine
from app.models import db as models

session = Session(bind=engine)


product = models.Product(name="Burger", price=10)
ingredients = [
    models.Ingredient(name="Beef", stock_quantity=20000),
    models.Ingredient(name="Cheese", stock_quantity=5000),
    models.Ingredient(name="Onion", stock_quantity=1000),
]
with Session(engine) as session:
    session.add(product)
    session.add_all(ingredients)
    session.flush()
    session.add(models.ProductIngredient(product_id=product.id, ingredient_id=ingredients[0].id, quantity=150))
    session.add(models.ProductIngredient(product_id=product.id, ingredient_id=ingredients[1].id, quantity=30))
    session.add(models.ProductIngredient(product_id=product.id, ingredient_id=ingredients[2].id, quantity=20))
    session.commit()
