from fastapi import FastAPI
from fastapi_pagination import add_pagination

from database.base import Base,engine
from routers import category_item_router
from routers.cateogry import category_router
from routers.basket import basket_router
from routers.auth import auth_router
from routers.staff import staff_router
from routers.user import user_router
from routers.item import item_router
from routers.order import order_router
app = FastAPI()
add_pagination(app)

app.include_router(auth_router, prefix="/v1",tags=["auth"])
app.include_router(user_router, prefix="/v1",tags=["user"])
app.include_router(staff_router, prefix="/v1", tags=["staff"])
app.include_router(item_router, prefix="/v1", tags=["item"])
app.include_router(category_router,prefix = '/v1',tags=["category"])
app.include_router(category_item_router,prefix = '/v1',tags=["category_item"])
app.include_router(basket_router,prefix="/v1", tags=["basket"])
app.include_router(order_router,prefix="/v1",tags=["order"])
app.include_router(basket_router,prefix="/v1", tags=["basket"])