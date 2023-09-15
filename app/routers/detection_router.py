from fastapi import FastAPI, Path, Header, Body, File, UploadFile, APIRouter
from app.utils.functions.string import get_unique_image_name
from app.utils.functions.file import delete_image_if_exists
from fastapi.responses import FileResponse

from app.models.detection_model import *
from app.models.detector_model import Detector

import datetime

router= APIRouter(
  prefix= '/detection'
)

@router.post('/{detector_id}')
async def add_detection(detector_id: int, detection_info: detection_pydantic_wtime):
    detector_ref= await Detector.get(id = detector_id)
    fullPlateNumber= detection_info.fullPlateNumber
    timeDetected= datetime.datetime.now()
    
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


