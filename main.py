from fastapi import FastAPI

from routers import meal_router, lunch_router
from models.models import Base
from database.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(meal_router.app, tags=['meal'])
app.include_router(lunch_router.app, tags=['lunch'])

