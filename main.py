from fastapi import FastAPI
from database.base import Base, engine
from routers.auth import auth_router
from routers.order import order_router
from routers.staff import staff_router
from routers.user import user_router
from routers.item import item_router

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/v1",tags=["auth"])
app.include_router(staff_router, prefix="/v1", tags=["staff"])
app.include_router(user_router, prefix="/v1",tags=["user"])
app.include_router(item_router, prefix="/v1", tags=["item"])
app.include_router(order_router, prefix="/v1", tags=["order"])
