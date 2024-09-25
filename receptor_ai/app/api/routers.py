from .users_auth import (
    fastapi_users_get_auth_router,
    fastapi_users_get_register_router,
    fastapi_users_get_reset_password_router,
    fastapi_users_get_verify_router,
)
from app.api.routing_intents_handlers import events_handler_router

all_routers = [
    fastapi_users_get_auth_router,
    fastapi_users_get_register_router,
    fastapi_users_get_reset_password_router,
    fastapi_users_get_verify_router,
    events_handler_router,
]
