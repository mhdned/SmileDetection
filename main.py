# Import libraries and dependencies
import os
import pathlib
import random
import string

from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from core import ai
from core.jinja import jinja

app = FastAPI(title="SmileDetection")

app.mount("/static", StaticFiles(directory="static"), name="static")


def file_iterator(file_path: str, chunk_size: int = 1024):
    with open(file_path, mode="rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk


def generate_random_string(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    description="This endpoint returns an HTML response with a message telling you if the api is working or not",
    tags=["API"],
    name="API checker",
    summary="Check if the API is live or not, just it",
    response_class=HTMLResponse,
)
async def api_check(request: Request):
    message = "FACE"
    context = {"message": message}
    return jinja.response(request=request, name="form.html", context=context)


@app.post(
    path="/process",
    description="Upload picture and prepare that for pass to AI model for processing and send result to client",
    status_code=status.HTTP_200_OK,
    summary="Main job of whole application",
    tags=["PROCESS", "API"],
    name="process",
)
async def upload_picture(request: Request, file: UploadFile = File(...)):
    main_path = os.path.dirname(os.path.abspath(__file__))
    upload_path = f"{main_path}/uploads"

    file_extension = file.filename.split(".")[-1].lower()

    if file_extension not in ["png", "jpg"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Only PNG and JPG are allowed.",
        )

    file_name = generate_random_string(10) + f".{file_extension}"

    uploaded_file_path = f"{upload_path}/{file_name}"

    with open(uploaded_file_path, "wb") as file_temp:
        file_temp.write(await file.read())

    result = ai.load_pic(uploaded_file_path)

    message = result

    context = {"message": message, "file_name": file_name}

    return jinja.response(request=request, name="result.html", context=context)


@app.get("/file/{file_name}")
async def show_file(file_name: str):
    main_path = os.path.dirname(os.path.abspath(__file__))
    upload_path = f"{main_path}/uploads"

    file_path = pathlib.Path(f"{upload_path}/{file_name}")

    if not file_path.exists() or not file_path.is_file():
        return {"error": "File not found"}
    return StreamingResponse(
        file_iterator(file_path),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
