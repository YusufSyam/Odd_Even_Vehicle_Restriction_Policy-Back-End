from fastapi import FastAPI, Path, Header, Body, File, UploadFile
from app.api.models.detector import *
from app.utils.functions.string import get_unique_image_name
from app.utils.functions.file import delete_image_if_exists
from fastapi.responses import FileResponse
from app.utils.const.const import IMAGE_FOLDER

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
    init_db(app)

@app.get('/')
def index():
    return {"key": "Hello World"}

@app.post('/detector')
async def add_detector(detector_info:detector_pydantic_in):
    roadName= detector_info.roadName
    city= detector_info.city
    description= detector_info.description
    province= detector_info.province
    roadName= detector_info.roadName
    subDistrict= detector_info.subDistrict
    ward= detector_info.ward

    image_data = base64.b64decode(detector_info.roadImagePath)
    image_name= get_unique_image_name(re.sub(r'\s+', '-', roadName.lower()))
    image_path = f"images/{image_name}"
    with open(image_path, "wb") as image:
        image.write(image_data)

    detector_data = {
        "roadName": roadName,
        "province": province,
        "city": city,  
        "subDistrict": subDistrict,
        "ward": ward,
        "roadImagePath": image_name,
        "description": description,
    }

    detector_obj = await Detector.create(**detector_data)
    response= await detector_pydantic.from_tortoise_orm(detector_obj)

    return {
        "status":"ok",
        "data": response
    }

@app .get('/detector/all')
async def get_detector_all():
    response= await detector_pydantic.from_queryset(Detector.all())

    return {
        "status":"ok",
        "data": response
    }

@app.get('/detector/{detector_id}')
async def get_detector_spesific(detector_id: int):
    response= await detector_pydantic.from_queryset_single(Detector.get(id=detector_id))

    return {
        "status":"ok",
        "data": response
    }

@app.put('/detector/{detector_id}')
async def update_detector(detector_id: int, update_info: detector_pydantic_in):
    detector= await Detector.get(id=detector_id)
    update_info= update_info.dict(exclude_unset=True)

    detector.city= update_info['city']
    detector.roadName= update_info['roadName']
    detector.province= update_info['province']
    detector.subDistrict= update_info['subDistrict']
    detector.ward= update_info['ward']
    detector.description= update_info['description']

    delete_image_if_exists(detector.roadImagePath)

    image_data = base64.b64decode(update_info['roadImagePath'])
    image_name= get_unique_image_name(re.sub(r'\s+', '-', update_info['roadName'].lower()))
    image_path = f"images/{image_name}"

    with open(image_path, "wb") as image:
        image.write(image_data)

    detector.roadImagePath= image_name
    print('Bikin Baru',detector.roadImagePath)

    await detector.save()

    response= await detector_pydantic.from_tortoise_orm(detector)

    return {
        "status":"ok",
        "data": response
    }

@app.get('/detector/card/all')
async def get_detector_card_all():
    data= await detector_pydantic.from_queryset(Detector.all())

    new_data= []

    for i in data:
        temp_obj= {
            "id": i.id,
            "roadName": i.roadName,
            "province": i.province,
            "city": i.city,
            "status": "Aktif",
            "detectedViolatorTotal": 53*int(i.id)-int(i.id),
            "passingVehicleTotal": 149  *int(i.id),
            "trafficConditions": "Macet",
            "notification": 0,
            "roadImagePath": i.roadImagePath
        }
        
        new_data.append(temp_obj)

    return {
        "status":"ok",
        "data": new_data
    }

@app.get("/get-image/{roadImagePath}")
async def get_image(roadImagePath: str):
    image_path = os.path.join(IMAGE_FOLDER, roadImagePath)

    if not os.path.isfile(image_path):  
        return {"message": "File not found"}

    return FileResponse(image_path, media_type="image/png")