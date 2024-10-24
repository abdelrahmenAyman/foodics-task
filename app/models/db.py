from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import event
from sqlmodel import Field, Relationship, SQLModel


class Base(SQLModel):
    __abstract__ = True
    __table_args__ = {"schema": "my_schema"}


class ProductIngredient(Base, table=True):
    product_id: int | None = Field(default=None, foreign_key="my_schema.product.id", primary_key=True)
    ingredient_id: int | None = Field(default=None, foreign_key="my_schema.ingredient.id", primary_key=True)
    quantity: int


class Product(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    ingredients: list["Ingredient"] = Relationship(back_populates="products", link_model=ProductIngredient)
    order_items: list["OrderItem"] = Relationship(back_populates="product")


class Ingredient(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    stock_quantity: int
    is_alerted: bool = Field(default=False)
    products: list[Product] = Relationship(back_populates="ingredients", link_model=ProductIngredient)
    threshold: int | None = Field(default=None)


@event.listens_for(Ingredient, "before_insert")
def compute_threshold(mapper, connection, target):
    target.threshold = target.stock_quantity // 2


class Order(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    order_items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order_id: int | None = Field(default=None, foreign_key="my_schema.order.id")
    product_id: int | None = Field(default=None, foreign_key="my_schema.product.id")
    product: Product = Relationship(back_populates="order_items")
    order: Order = Relationship(back_populates="order_items")
    quantity: int
