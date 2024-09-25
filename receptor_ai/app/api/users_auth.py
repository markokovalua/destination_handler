from app.schemas.users_auth import UserRead, UserCreate
from app.services.users_auth import auth_backend, fastapi_users


fastapi_users_get_auth_router = dict(
    router=fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
fastapi_users_get_register_router = dict(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
fastapi_users_get_reset_password_router = dict(
    router=fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"]
)
fastapi_users_get_verify_router = dict(
    router=fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"]
)
