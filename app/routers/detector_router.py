from fastapi import FastAPI, Path, Header, Body, File, UploadFile, APIRouter
from fastapi.responses import FileResponse

from tortoise import Tortoise
from app.models.detector_model import *
from app.models.detection_model import Detection

from app.utils.functions.string import get_unique_image_name
from app.utils.functions.file import delete_image_if_exists
from app.utils.const.directory import ROAD_IMAGE_FOLDER, DETECTION_IMAGE_FOLDER

import base64
from io import BytesIO
import os

import re

router = APIRouter(
    prefix='/detector'
)


@router.post('/')
async def add_detector(detector_info: detector_pydantic_in):
    roadName = detector_info.roadName
    city = detector_info.city
    description = detector_info.description
    province = detector_info.province
    roadName = detector_info.roadName
    subDistrict = detector_info.subDistrict
    ward = detector_info.ward

    image_data = base64.b64decode(detector_info.roadImagePath)
    image_name = get_unique_image_name(re.sub(r'\s+', '-', roadName.lower()))
    image_path = f"{ROAD_IMAGE_FOLDER}/{image_name}"
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
    response = await detector_pydantic.from_tortoise_orm(detector_obj)

    return {
        "status": "ok",
        "data": response
    }


@router.get('/')
async def get_detector_all():
    response = await detector_pydantic.from_queryset(Detector.all())

    return {
        "status": "ok",
        "data": response
    }


@router.get('/{detector_id}')
async def get_detector_spesific(detector_id: int):
    response = await detector_pydantic.from_queryset_single(Detector.get(id=detector_id))

    return {
        "status": "ok",
        "data": response
    }


@router.put('/{detector_id}')
async def update_detector(detector_id: int, update_info: detector_pydantic_in):
    detector = await Detector.get(id=detector_id)
    update_info = update_info.dict(exclude_unset=True)

    detector.city = update_info['city']
    detector.roadName = update_info['roadName']
    detector.province = update_info['province']
    detector.subDistrict = update_info['subDistrict']
    detector.ward = update_info['ward']
    detector.description = update_info['description']

    delete_image_if_exists(ROAD_IMAGE_FOLDER, detector.roadImagePath)

    image_data = base64.b64decode(update_info['roadImagePath'])
    image_name = get_unique_image_name(
        re.sub(r'\s+', '-', update_info['roadName'].lower()))
    image_path = f"images/{image_name}"

    with open(image_path, "wb") as image:
        image.write(image_data)

    detector.roadImagePath = image_name
    print('Bikin Baru', detector.roadImagePath)

    await detector.save()

    response = await detector_pydantic.from_tortoise_orm(detector)

    return {
        "status": "ok",
        "data": response
    }


@router.delete('/{detector_id}')
async def delete_detector(detector_id: int):
    selected_detector = await Detector.filter(id=detector_id).first()

    if selected_detector:
        related_detections= await Detection.filter(detector_id=selected_detector.id)

        for detection in related_detections:
            print(f"Deleting Detection ID: {detection.id}")
            
            delete_image_if_exists(DETECTION_IMAGE_FOLDER, detection.imagePath)
            await detection.delete()
        
        delete_image_if_exists(ROAD_IMAGE_FOLDER, selected_detector.roadImagePath)
        await selected_detector.delete()
    else:
        raise HTTPException(status_code=404, detail="Detector not found")

    return {
        "status": "ok"
    }


@router.get('/card/all')
async def get_detector_card_all():
    data = await detector_pydantic.from_queryset(Detector.all())

    new_data = []

    for i in data:
        temp_obj = {
            "id": i.id,
            "roadName": i.roadName,
            "province": i.province,
            "city": i.city,
            "status": "Aktif",
            "detectedViolatorTotal": 53*int(i.id)-int(i.id),
            "passingVehicleTotal": 149 * int(i.id),
            "trafficConditions": "Macet",
            "notification": 0,
            "roadImagePath": i.roadImagePath
        }

        new_data.append(temp_obj)

    return {
        "status": "ok",
        "data": new_data
    }


@router.get('/history/detection-summary/{detector_id}')
async def get_detection_history_summary_by_detector(detector_id: int):
    sql_query = f"SELECT id, detectionDate, COUNT(*) AS passingVehicleTotal, SUM(isViolating) AS detectedViolatorTotal, SUM(plateType = 'genap') AS evenPlatedVehicle, SUM(plateType = 'ganjil') AS oddPlatedVehicle FROM detection WHERE detector_id = {detector_id} GROUP BY detectionDate ORDER BY detectionDate"
    temp_detection_summary = await Tortoise.get_connection("default").execute_query(sql_query)

    detection_summary = list(temp_detection_summary)[-1]

    detector_info = await detector_pydantic.from_queryset_single(Detector.get(id=detector_id))

    response = {
        "detector": detector_info,
        "detectionSummaryList": detection_summary
    }

    return {
        "status": "ok",
        "data": response
    }


@router.get('/get-min-date/{detector_id}')
async def get_min_date_of_detector(detector_id: int):
    sql_query = f"SELECT MIN(detectionDate) AS latestDetectionDate FROM detection WHERE detector_id = {detector_id}"
    temp_result = await Tortoise.get_connection("default").execute_query(sql_query)
    response = list(temp_result)[-1][0]

    return {
        "status": "ok",
        "data": response
    }
