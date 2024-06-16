from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, UploadFile, Header, status
from fastapi.responses import JSONResponse

from src.PatentLoader.FileLoader import FileLoader
from src.auth.user_service import UserService, get_user_service

app_router = APIRouter(prefix="/api")


@app_router.post("/upload/{user_id}")
async def upload_data(
    user_id: int,
    file: UploadFile,
    authorization: Annotated[str, Header()],
    service: Annotated[UserService, get_user_service],
) -> JSONResponse:
    access_token = authorization.split()[-1]
    user = await service.fetch_by_token(access_token)

    if user is None or user.id != user_id:
        return JSONResponse(
            {"detail": "Для загрузки файла нужно войти в свой аккаунт."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    path = Path(f"/data/uploaded/{user.username}/{file.filename}")
    with path.open(mode="bw") as fout:
        fout.write(file.read())

    loader = FileLoader()
    await loader.load_file(str(path))

    path = f"/data/processed/{user.username}/{file.filename}"
    loader.patent_linker.export_final_dataframe_to_excel(path)

    return JSONResponse({})
