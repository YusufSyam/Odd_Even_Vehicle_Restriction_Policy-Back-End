from fastapi import FastAPI, Path, Header, Body, File, UploadFile
from app.utils.functions.string import get_unique_image_name
from app.utils.functions.file import delete_image_if_exists
from fastapi.responses import FileResponse
from app.utils.const.directory import ROAD_IMAGE_FOLDER
from tortoise.contrib.fastapi import register_tortoise

# Router
from app.routers import detector_router, detection_router

# Gambar
import base64
from io import BytesIO
import PIL.Image
from IPython.display import display
import os

import re

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup_db():
    # init_db(app)
    register_tortoise(
        app,
        db_url='mysql://root@127.0.0.1:3307/oevrp',
        modules={'models': ['app.models.detection_model',
                            'app.models.detector_model', 'app.models.detection_details_model']},
        generate_schemas=True,
        add_exception_handlers=True
    )


@app.get('/')
def index():
    return {"key": "Hello World"}


app.include_router(detector_router.router)
app.include_router(detection_router.router)


@app.get("/get-image/{roadImagePath}")
async def get_image(roadImagePath: str):
    image_path = os.path.join(ROAD_IMAGE_FOLDER, roadImagePath)

    if not os.path.isfile(image_path):
        return {"message": "File not found"}

    return FileResponse(image_path, media_type="image/png")
