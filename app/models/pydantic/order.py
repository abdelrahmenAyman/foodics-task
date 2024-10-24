from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models import db as models


class OrderItem(BaseModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity_positive_integer(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity cannot be negative or zero.")
        return v


class OrderCreate(BaseModel):
    order_items: list[OrderItem] = Field(alias="products")

    @field_validator("order_items")
    @classmethod
    def validate_order_items_not_empty(cls, v: list[OrderItem]) -> list[OrderItem]:
        if not v:
            raise ValueError("Products field cannot be empty.")
        return v


class OrderRead(BaseModel):
    id: int
    created_at: datetime
    order_items: list[models.OrderItem]
