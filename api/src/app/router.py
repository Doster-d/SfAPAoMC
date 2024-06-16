from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, UploadFile, Header, status, Depends
from fastapi.responses import JSONResponse, FileResponse, Response

from src.PatentLoader.FileLoader import FileLoader
from src.CompanyCategory.OrgClassificator import OrgClassificator
from src.auth.user_service import UserService, get_user_service

from .file_service import FileService, get_file_service

__all__ = [
    "router",
]

router = APIRouter(prefix="/api")


@router.post("/upload/{user_id}")
async def upload_data(
    user_id: int,
    file: UploadFile,
    authorization: Annotated[str, Header()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> JSONResponse:
    access_token = authorization.split()[-1]
    user = await user_service.fetch_by_token(access_token)

    if user is None or user.id != user_id:
        return JSONResponse(
            {"detail": "Для загрузки файла нужно войти в свой аккаунт."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    path = Path(f"/data/uploaded/{user.username}/{file.filename}")
    path.parent.mkdir(exist_ok=True, parents=True)
    path.touch()
    with path.open(mode="bw") as fout:
        fout.write(await file.read())

    loader = FileLoader()
    await loader.load_file(str(path))

    loader.patent_linker.export_final_dataframe_to_excel(path)

    file_id = await file_service.create(user.id, str(path))

    return JSONResponse(
        {
            "filename": file.filename,
            "fileId": file_id,
        }
    )


@router.get("/download/{user_id}/{file_id}")
async def download_data(
    user_id: int,
    file_id: int,
    authorization: Annotated[str, Header()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> Response:
    access_token = authorization.split()[-1]
    user = await user_service.fetch_by_token(access_token)

    if user is None or user.id != user_id:
        return JSONResponse(
            {"detail": "Для загрузки файла нужно войти в свой аккаунт"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    file = await file_service.fetch_by_id(file_id)

    if file is None:
        return JSONResponse(
            {"detail": "Файл не найден"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return FileResponse(file.path)


@router.get("/information/{user_id}/{file_id}")
async def fetch_information(
    user_id: int,
    file_id: int,
    authorization: Annotated[str, Header()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> JSONResponse:
    access_token = authorization.split()[-1]
    user = await user_service.fetch_by_token(access_token)

    if user is None or user.id != user_id:
        return JSONResponse(
            {"detail": "Для загрузки файла нужно войти в свой аккаунт"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    file = await file_service.fetch_by_id(file_id)

    if file is None:
        return JSONResponse(
            {"detail": "Файл не найден"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    classificator = OrgClassificator()
    loader = FileLoader()
    await loader.load_file(file.path)

    data = loader.patent_processor.patents_ids["company_id"].to_list()
    classificator.classify_company(data)

    return classificator.classification
