from fastapi import FastAPI, Path, Header, Body, File, UploadFile, APIRouter
from app.utils.functions.string import get_unique_image_name
from app.utils.functions.file import delete_image_if_exists
from fastapi.responses import FileResponse

from tortoise.expressions import Q

from app.models.detection_model import *

from app.utils.const.directory import DETECTION_IMAGE_FOLDER
from app.utils.functions.string import get_unique_image_name
from app.utils.functions.date import parse_date_detection

import base64
from io import BytesIO
import os
import re

from datetime import datetime, timedelta

router = APIRouter(
    prefix='/detection'
)


@router.get('/')
async def get_detection_all():
    response = await Detection.all()

    return {
        "status": "ok",
        "data": response
    }


@router.post('/{detector_id}/{detection_date}')
async def add_detection(detector_id: int, detection_date:str, detection_info: detection_pydantic_in):
    detector_ref = await Detector.get(id=detector_id)
    fullPlateNumber = detection_info.fullPlateNumber
    plateNumber = detection_info.plateNumber
    isViolating = detection_info.isViolating
    plateType = detection_info.plateType
    policyAtTheMoment = detection_info.policyAtTheMoment

    image_data = base64.b64decode(detection_info.imagePath)
    image_name = get_unique_image_name(f'{detector_id}-{fullPlateNumber}')
    image_path = f"{DETECTION_IMAGE_FOLDER}/{image_name}"
    with open(image_path, "wb") as image:
        image.write(image_data)

    detection_data = {
        "fullPlateNumber": fullPlateNumber,
        "plateNumber": plateNumber,
        "isViolating": isViolating,
        "plateType": plateType,
        "policyAtTheMoment": policyAtTheMoment,
        "imagePath": image_name,
        "detectionDate": parse_date_detection(detection_date)
    }

    detection_obj = await Detection.create(**detection_data, detector=detector_ref)
    response = await detection_pydantic.from_tortoise_orm(detection_obj)

    return {
        "status": "ok",
        "response": response
    }


@router.get('/{detector_id}')
async def get_detection_by_detector(detector_id: int):
    response = await Detection.filter(detector_id=detector_id)

    print(response)

    return {
        "status": "ok",
        "data": response
    }

@router.delete('/{detection_id}')
async def delete_detection(detection_id: int):
    selected_detection = await Detection.filter(id=detection_id).first()

    if not selected_detection:
        raise HTTPException(status_code=404, detail="Detection not found")

    delete_image_if_exists(DETECTION_IMAGE_FOLDER, selected_detection.imagePath)
    await selected_detection.delete()

    return {
        "status": "ok"
    }


@router.get('/{detector_id}/{date}')
async def get_detection_by_detector_time(detector_id: int, date: str):
    detection_date = datetime.strptime(date, "%Y-%m-%d")
    
    detection_list = await Detection.filter(
        detector_id=detector_id,
        detectionDate=detection_date
    )

    detector_info = await Detector.get(id=detector_id)

    response = {
      "detector" : detector_info,
      "detectionList" : detection_list
    }

    return {
        "status": "ok",
        "data": response
    }

