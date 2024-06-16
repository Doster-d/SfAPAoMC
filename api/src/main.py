import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .auth import router as auth_router


api = FastAPI(
    prefix="/api",
    title="MLProject",
    debug=True,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(f"EXCEPTIOn={traceback.format_exc()}")
        return JSONResponse({"detail": "Что-то пошло не так"}, status_code=500)


api.middleware("http")(catch_exceptions_middleware)
# api.include_router(api_router)
api.include_router(auth_router)