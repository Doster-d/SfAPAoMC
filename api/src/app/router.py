from uuid import uuid4
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

singleton_instance = OrgClassificator()


def get_classificator() -> OrgClassificator:
    return singleton_instance


@router.post("/upload/{user_id}")
async def upload_data(
    user_id: int,
    file: UploadFile,
    authorization: Annotated[str, Header()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    file_service: Annotated[FileService, Depends(get_file_service)],
    classificator: Annotated[OrgClassificator, Depends(get_classificator)],
) -> JSONResponse:
    access_token = authorization.split()[-1]
    user = await user_service.fetch_by_token(access_token)

    if user is None or user.id != user_id:
        return JSONResponse(
            {"detail": "Для загрузки файла нужно войти в свой аккаунт."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    path = Path(f"/data/uploaded/{str(uuid4())}_{file.filename}")
    path.parent.mkdir(exist_ok=True, parents=True)
    path.touch()
    with path.open(mode="bw") as fout:
        fout.write(await file.read())

    loader = FileLoader()
    await loader.load_file(str(path))
    await loader.process_file()

    loader.patent_linker.export_final_dataframe_to_excel(path)

    data = classificator.get_company_ids_from_excel(path)
    await classificator.classify_company(
        data,
        classify_categories=False,
        target_classifier=classificator.global_classification[
            loader.patent_processor.patent_type
        ],
    )
    await classificator.classify_company(data)

    file_id = await file_service.create(user.id, str(path))

    return JSONResponse(
        {
            "filename": file.filename,
            "fileId": file_id,
        }
    )


@router.get("/download/{file_id}")
async def download_data(
    file_id: int,
    file_service: Annotated[FileService, Depends(get_file_service)],
) -> Response:
    file = await file_service.fetch_by_id(file_id)

    if file is None:
        return JSONResponse(
            {"detail": "Файл не найден"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return FileResponse(file.path)


@router.get("/information/{file_id}")
async def fetch_information(
    file_id: int,
    file_service: Annotated[FileService, Depends(get_file_service)],
    classificator: Annotated[OrgClassificator, Depends(get_classificator)],
) -> JSONResponse:
    file = await file_service.fetch_by_id(file_id)

    if file is None:
        return JSONResponse(
            {"detail": "Файл не найден"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return classificator.classification


@router.get("/information")
async def fetch_all_information(
    classificator: Annotated[OrgClassificator, Depends(get_classificator)],
) -> JSONResponse:
    return classificator.global_classification
