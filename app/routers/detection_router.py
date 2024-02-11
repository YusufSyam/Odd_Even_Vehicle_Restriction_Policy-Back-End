from fastapi import FastAPI, Path, Header, Body, File, UploadFile, APIRouter, Form
from fastapi.responses import FileResponse
from typing import List
from tortoise import fields, Tortoise
import cv2

from tortoise.expressions import Q
from app.models.detection_model import Detection

from app.models.detection_model import *

from app.utils.const.directory import DETECTION_IMAGE_FOLDER, TEMPORARY_IMAGE_FOLDER, CAR_IMAGE_FOLDER, FRAME_IMAGE_FOLDER
from app.utils.const.dummy import dummy_new_detection
from app.utils.functions.string import get_unique_image_name, generate_unique_string, get_detector_id
from app.utils.functions.file import delete_image_if_exists, decode_and_save_image, save_image
from app.utils.functions.date import parse_date_detection

# Model
from app.detect import *

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


@router.get('/newest')
async def get_detection_newest():
    response = await Detection.filter().order_by(
        '-detectionDate', '-detectionTime'
    )

    return {
        "status": "ok",
        "data": response
    }


@router.post('/{detector_id}/{detection_date}')
async def add_detection(detector_id: int, detection_date: str, detection_info: detection_pydantic_in):
    detector_ref = await Detector.get(id=detector_id)
    fullPlateNumber = detection_info.fullPlateNumber
    plateNumber = detection_info.plateNumber
    isViolating = detection_info.isViolating
    plateType = detection_info.plateType
    policyAtTheMoment = detection_info.policyAtTheMoment

    image_name = get_unique_image_name(f'{detector_id}-{fullPlateNumber}')
    decode_and_save_image(detection_info.imagePath, image_name, DETECTION_IMAGE_FOLDER)

    car_image_name= ''
    frame_image_name= ''

    if len(detection_info.carImagePath)>0:
        car_image_name= f'car-{image_name}'
        decode_and_save_image(detection_info.carImagePath, car_image_name, CAR_IMAGE_FOLDER)

    if len(detection_info.frameImagePath)>0:
        frame_image_name= f'frame-{image_name}'
        decode_and_save_image(detection_info.frameImagePath, frame_image_name, FRAME_IMAGE_FOLDER)
    
    detection_data = {
        "fullPlateNumber": fullPlateNumber,
        "plateNumber": plateNumber,
        "isViolating": isViolating,
        "plateType": plateType,
        "policyAtTheMoment": policyAtTheMoment,
        "detectionDate": parse_date_detection(detection_date),
        "imagePath": image_name,
        "carImagePath": car_image_name,
        "frameImagePath": frame_image_name
    }

    detection_obj = await Detection.create(**detection_data, detector=detector_ref)
    response = await detection_pydantic.from_tortoise_orm(detection_obj)

    return {
        "status": "ok",
        "response": response
    }


@router.post('/manual-detection/{detector_id}/{detection_date}')
async def add_manual_detection(detector_id: int, detection_date: str, detection_info_list: List[detection_pydantic_in]):
    new_detections = []
    detector_ref = await Detector.get(id=detector_id)
    detection_date_parsed = parse_date_detection(detection_date)

    print(detection_info_list)
    for detection_info in detection_info_list:
        try:
            fullPlateNumber = detection_info.fullPlateNumber
            plateNumber = detection_info.plateNumber
            isViolating = detection_info.isViolating
            plateType = detection_info.plateType
            policyAtTheMoment = detection_info.policyAtTheMoment
            carImagePath = detection_info.carImagePath
            frameImagePath = detection_info.frameImagePath
            image_name = detection_info.imagePath

            # Di sini nanti bikin fungsi yang kasi pindah gambar dari temp manual detection folder ke images/detection
            # temp manual detection folder itu folder pas manual deteksi yang akan dibersihkan dalam 12 jam
            # image_data = base64.b64decode(detection_info.imagePath)
            # image_name = get_unique_image_name(f'{detector_id}-{fullPlateNumber}')
            # image_path = f"{DETECTION_IMAGE_FOLDER}/{image_name}"
            # with open(image_path, "wb") as image:
            #     image.write(image_data)

            detection_data = {
                "fullPlateNumber": fullPlateNumber,
                "plateNumber": plateNumber,
                "isViolating": isViolating,
                "plateType": plateType,
                "policyAtTheMoment": policyAtTheMoment,
                "carImagePath": carImagePath,
                "frameImagePath": frameImagePath,
                "imagePath": image_name,
                "detectionDate": detection_date_parsed
            }

            detection_obj = await Detection.create(**detection_data, detector=detector_ref)

            print(f"Sukses menambahkan data plat {fullPlateNumber}")
        except Exception as e:
            # Menangani kesalahan dan mengembalikan pesan kesalahan
            error_message = f"Failed to add detector: {str(e)}"
            return HTTPException(status_code=400, detail=error_message)

    response = detection_info_list
    return {
        "status": "ok",
        "response": response
    }


@router.get('/{detector_id}')
async def get_detection_by_detector(detector_id: int):
    response = await Detection.filter(detector_id=detector_id)
    # .order_by(
    #     '-detectionDate', '-detectionTime'
    # )

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

    delete_image_if_exists(DETECTION_IMAGE_FOLDER,
                           selected_detection.imagePath)
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
        "detector": detector_info,
        "detectionList": detection_list
    }

    return {
        "status": "ok",
        "data": response
    }


@router.post("/manual-detection/upload-file/")
async def upload_manual_detection_file(
    file: UploadFile = File(...)
):
    image_name= file.filename
    save_image(file.file.read(), image_name, TEMPORARY_IMAGE_FOLDER)

    image = cv2.imread(f'{TEMPORARY_IMAGE_FOLDER}/{image_name}')

    detection_result= detect_plate_on_sent_image(image, temp_img_path=image_name, detect_type="manual")

    delete_image_if_exists(TEMPORARY_IMAGE_FOLDER, image_name)

    response = {
        "detection_list": detection_result
    }

    return {
        "status": "ok",
        "data": response
    }


@router.get("/get-detection-image-list/")
async def get_detection_image_list():
    try:
        image_list = [file for file in os.listdir(DETECTION_IMAGE_FOLDER) if file.lower(
        ).endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        return {
            "status": "ok",
            "data": image_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-temporary-image-list/")
async def get_temporary_image_list():
    try:
        image_list = [file for file in os.listdir(TEMPORARY_IMAGE_FOLDER) if file.lower(
        ).endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        return {
            "status": "ok",
            "data": image_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/delete-detection-image/{image_path}')
async def delete_detection_image(image_path: str):
    delete_image_if_exists(DETECTION_IMAGE_FOLDER, image_path)

    return {
        "status": f'Image {image_path} succesfully deleted'
    }

@router.delete('/delete-temporary-image/{image_path}')
async def delete_temp_image(image_path: str):
    delete_image_if_exists(TEMPORARY_IMAGE_FOLDER, image_path)

    return {
        "status": f'Temporary Image {image_path} succesfully deleted'
    }

# Jadi di sini nanti akan diganti menjadi langsung diproses
@router.post('/send-image-to-detect/')
async def send_image_to_detect(imageFile: UploadFile = File(...)):
    temp_image_name = f'{generate_unique_string()}_{imageFile.filename}'
    detector_id= get_detector_id(imageFile.filename)

    save_image(imageFile.file.read(), temp_image_name, TEMPORARY_IMAGE_FOLDER)
    
    temp_image_path = f"{TEMPORARY_IMAGE_FOLDER}/{temp_image_name}"
    image = cv2.imread(temp_image_path)

    detection_list= detect_plate_on_sent_image(image, temp_image_name, imageFile.filename, detect_type="kamera")
    detection_response_list= []

    for detection_result in detection_list:
        detector_ref = await Detector.get(id=detector_id)
        
        detection_data = {
            "fullPlateNumber": detection_result["fullPlateNumber"],
            "plateNumber": detection_result["plateNumber"],
            "isViolating": detection_result["isViolating"],
            "plateType": detection_result["plateType"],
            "policyAtTheMoment": detection_result["policyAtTheMoment"],
            "detectionDate": detection_result["detectionDate"],
            "detectionTime": detection_result["detectionTime"],
            "imagePath": detection_result["imagePath"],
            "carImagePath": detection_result["carImagePath"],
            "frameImagePath": detection_result["frameImagePath"],
        }

        detection_response_list.append(detection_data)

        detection_obj = await Detection.create(**detection_data, detector=detector_ref)
    # response = await detection_pydantic.from_tortoise_orm(detection_obj)

    return {
        "status": "ok",
        "response": detection_response_list
    }

    # return {
    #     "status": f'Terjadi Error Saat Pengunggahan Gambar dan Penyimpanan Data'
    # }

# @router.post('/upload-temporary-image/')
# async def upload_detection_image(image_path: str, image_name: str):
#     image_data = base64.b64decode(image_path)

#     if image_name is None or len(image_name) == 0:
#         image_name = generate_unique_string()

#     image_path = f"{TEMPORARY_IMAGE_FOLDER}/{image_name}"
#     with open(image_path, "wb") as image:
#         image.write(image_data)

#     return {
#         "status": f'Temporary image {image_path} succesfully uploaded'
#     }

@router.post("/print-type/")
async def print_data_type(data: str):
    return {"data_type": str(type(data).__name__), "data_value": data}

# DASHBOARD / ANALYTICS
# @router.get('/get-violator-total-by-date/{date}')
# async def get_violator_total_by_date(date: str):
#     print(date,'date')
#     try:
#         result = await Detection.filter(detectionDate=query_date).values(
#             pelanggar=Sum(Case(When(isViolating=True, then=1), default=0)),
#             patuh=Sum(Case(When(isViolating=False, then=1), default=0))
#         )
#         return {
#             'status':'ok',
#             'data': result[0]
#         }
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))
