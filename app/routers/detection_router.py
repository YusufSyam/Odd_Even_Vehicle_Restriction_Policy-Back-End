from fastapi import FastAPI, Path, Header, Body, File, UploadFile, APIRouter
from app.utils.functions.string import get_unique_image_name
from app.utils.functions.file import delete_image_if_exists
from fastapi.responses import FileResponse

from app.models.detection_model import *
from app.models.detector_model import Detector

import base64
from io import BytesIO
import os
import re

import datetime

router= APIRouter(
  prefix= '/detection'
)

@router.post('/{detector_id}')
async def add_detection(detector_id: int, detection_info: detection_pydantic_in):
    detector_ref= await Detector.get(id = detector_id)
    fullPlateNumber= detection_info.fullPlateNumber
    plateNumber= detection_info.plateNumber
    isViolating= detection_info.isViolating
    plateType= detection_info.plateType
    policyAtTheMoment= detection_info.policyAtTheMoment
    
    timeDetected= datetime.datetime.now()

    # image_data = base64.b64decode(detector_info.roadImagePath)
    # image_name= f'{detector_id}-{fullPlateNumber}-{timeDetected}'
    # image_path = f"{ROAD_IMAGE_FOLDER}/{image_name}"
    # with open(image_path, "wb") as image:
    #     image.write(image_data)
    
    detection_data= {
        "fullPlateNumber": fullPlateNumber,
        "timeDetected": timeDetected
    }

    detection_obj = await Detection.create(**detection_data, detector=detector_ref)
    response= await detection_pydantic.from_tortoise_orm(detection_obj)

    return {
      "status": "ok",
      "response": response
    }


