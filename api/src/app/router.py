from pathlib import Path

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from src.PatentLoader.FileLoader import FileLoader

app_router = APIRouter(prefix="/api")


@app_router.post("/upload/{user_id}")
async def upload_data(user_id: int, file: UploadFile) -> JSONResponse:
    path = Path(f"/data/{file.filename}")
    with path.open(mode="bw") as fout:
        fout.write(file.read())

    loader = FileLoader()
    loader.load_file(str(path))
