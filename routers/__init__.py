from .basket import basket_router
from .cateogry import category_router
from .item import item_router
from .order import order_router
from .user import user_router
from .auth import auth_router
from .staff import staff_router
from  .category_item import category_item_router



routers = [
    user_router,
    item_router,
    auth_router,
    order_router,
    staff_router,
    basket_router,
    category_router,
    category_item_router
]
