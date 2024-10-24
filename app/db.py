from sqlalchemy import text
from sqlmodel import SQLModel, create_engine

from app.models import *
from app.settings import settings

engine = create_engine(settings.DB_URL)


def initialize_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS my_schema;"))
        conn.commit()
    SQLModel.metadata.create_all(bind=engine)


def dispose_db():
    SQLModel.metadata.schema = "my_schema"
    SQLModel.metadata.drop_all(bind=engine)
