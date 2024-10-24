from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from app import actions
from app.dependencies import get_session
from app.errors import IngredientStockNotEnough
from app.models import db as models
from app.models.pydantic.order import OrderCreate

router = APIRouter()


@router.post("/orders", response_model=models.Order, status_code=201)
async def create_order(data: OrderCreate, session: Session = Depends(get_session)):
    try:
        order = await actions.Order.create(order_items=data.order_items, session=session)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail="Product ID is not found")
    except IngredientStockNotEnough as e:
        raise HTTPException(status_code=400, detail=str(e))

    return order
