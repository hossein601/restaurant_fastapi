from .item import item_router
from .order import order_router
from .reserve import reserve_router
from .user import user_router
from .auth import auth_router
from.staff import staff_router


routers = [
    user_router,
    item_router,
    auth_router,
    order_router,
    staff_router,
    reserve_router
]
