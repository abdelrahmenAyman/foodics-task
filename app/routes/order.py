from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from app import actions
from app.dependencies import get_session
from app.errors import IngredientStockNotEnough
from app.models import db as models
from app.models.pydantic.order import OrderCreate, OrderRead

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


@router.get("/orders", response_model=list[OrderRead])
async def list_orders(
    offset: int = 0, limit: int = Query(default=100, le=100), session: Session = Depends(get_session)
):
    return await actions.Order.list(offset=offset, limit=limit, session=session)
