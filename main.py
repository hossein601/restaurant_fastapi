from fastapi import FastAPI
from database.base import Base, engine
from routers import auth_router
from routers.order import order_router
from routers.reserve import reserve_router
from routers.staff import staff_router
from routers.user import user_router
from routers.item import item_router

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth_router, prefix="/v1")
app.include_router(staff_router, prefix="/v1")
app.include_router(reserve_router, prefix="/v1")
app.include_router(user_router, prefix="/v1")
app.include_router(item_router, prefix="/v1")
app.include_router(order_router, prefix="/v1")
