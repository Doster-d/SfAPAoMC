from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from .schemas import CreateUserScheme, LoginUserResult, LoginUserScheme
from .user_service import UserService, get_user_service

__all__ = [
    "router",
]

router = APIRouter(prefix="/api")


@router.post("/signup")
async def create_user(
    create_user_data: CreateUserScheme, service: UserService = Depends(get_user_service)
) -> JSONResponse:
    user = await service.fetch_by_email(create_user_data.email)

    if user is not None:
        return JSONResponse(
            {
                "detail": "Пользователь с такой почтой уже зарегистрирован",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    await service.create_user(create_user_data)
    return JSONResponse({})


@router.post("/signin")
async def login_user(
    user_login_data: LoginUserScheme, service: UserService = Depends(get_user_service)
) -> LoginUserResult:
    user = await service.fetch_by_email(user_login_data.email)

    if user is None:
        return JSONResponse(
            {
                "detail": "Неверный пароль или логин",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not service.verify_password(user, user_login_data.password):
        return JSONResponse(
            {
                "detail": "Неверный пароль или логин",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    token = await service.create_access_token(user)

    return LoginUserResult(
        username=user.username,
        email=user.email,
        accessToken=token,
        userId=user.id,
    )
