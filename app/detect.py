from app.utils.functions.date import parse_date_detection, get_current_date, get_current_time
from app.utils.functions.string import get_unique_image_name
from app.utils.functions.file import delete_image_if_exists, decode_and_save_image, save_image, save_image_cv


from app.utils.const.directory import BASE_DIR, DETECTION_IMAGE_FOLDER, TEMPORARY_IMAGE_FOLDER, CAR_MODEL_PATH, CAR_IMAGE_FOLDER, FRAME_IMAGE_FOLDER, LICENSE_PLATE_MODEL_PATH

from app.utils.detection_utils.detect_utils import *
from app.utils.detection_utils.plate_validation import validate_raw_plate_text
from app.utils.detection_utils.image_preprocess import *
from app.utils.detection_utils.ocr_utils import *
from app.utils.detection_utils.sort import *

from ultralytics import YOLO
import cv2
import time
import torch

import logging

import os

coco_model = YOLO(CAR_MODEL_PATH)
license_plate_detector = YOLO(LICENSE_PLATE_MODEL_PATH)

# Menyimpan file log di direktori 'logs'
log_file_path = os.path.join(BASE_DIR, 'logs', 'detection_history.log')

logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s (%(levelname)s) - %(message)s')


def oevlpr_detection(frame, filename='', upscale_amount=6, vertical_stretch=0.6, opening_kernel_size=(3, 3), apply_remove_noise=False, apply_straightened_twice= False, apply_bitwise_not= False, apply_opening=False, thresholding_type=1):
    global coco_model, license_plate_detector

    detection_list = []

    detections = coco_model(frame, conf=0.01)[0]
    car_detections_list= detections.boxes.data.tolist()

    detected_car = []
    for detection in car_detections_list:
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) == 2:
            detected_car.append([x1, y1, x2, y2, score])

    detected_car_history = np.array(detected_car)

    identifier = filename.split('.')[0]

    license_plates = license_plate_detector(frame)[0]

    is_frame_img_made = False

    license_plates_list= license_plates.boxes.data.tolist()
    
    logging.info(f'Pada {filename} terdeteksi {len(license_plates_list)} plat kendaraan')

    for license_plate in license_plates_list:
        x1, y1, x2, y2, score, class_id = license_plate

        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, detected_car_history)
        xcar1, ycar1, xcar2, ycar2 = limit_at_zero(xcar1), limit_at_zero(
            ycar1), limit_at_zero(xcar2), limit_at_zero(ycar2)

        if y2-y1 < x2-x1:
            car_crop = frame[int(ycar1):int(ycar2), int(xcar1): int(xcar2), :]
            license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

            # process license plate
            license_plate_crop_gray = cv2.cvtColor(
                license_plate_crop, cv2.COLOR_BGR2GRAY)

            license_plate_crop_straight, is_straightened = straightening_image(license_plate_crop_gray)

            license_plate_crop_straight = upscale_image(license_plate_crop_straight, upscale_amount)

            if apply_remove_noise:
                license_plate_crop_straight= remove_noise(license_plate_crop_straight)

            if thresholding_type==1:
                license_plate_crop_thresh = thresholding1(license_plate_crop_straight)
            else:
                license_plate_crop_thresh = thresholding2(license_plate_crop_straight)

            if apply_opening:
                license_plate_crop_thresh= opening(license_plate_crop_thresh, opening_kernel_size)
            
            if apply_bitwise_not:
                license_plate_crop_thresh= cv2.bitwise_not(license_plate_crop_thresh)

                license_plate_crop_thresh= stretch_vertical(license_plate_crop_thresh, vertical_stretch)

            if apply_straightened_twice:
                license_plate_crop_thresh, is_straightened2 = straightening_image(license_plate_crop_thresh)

            # read license plate number
            license_plate_text, license_plate_text_score = read_license_plate(
                license_plate_crop_thresh)

            if license_plate_text is not None and len(license_plate_text)>=5:
                # if license_plate_text is not None:
                if not is_frame_img_made:
                    frame_image_filename = f"{filename}"
                    cv2.imwrite(f'{FRAME_IMAGE_FOLDER}/{frame_image_filename}', frame)

                    is_frame_img_made = True

                temp_filename= get_unique_image_name(identifier)
                car_image_filename = f'car-{temp_filename}'
                
                
                if car_id==-1 or xcar1==-1:
                    car_image_filename= None
                else:
                    # car_image_filename = os.path.join(TEMP_CAR_IMG_DIR, f"car_id:{car_id}-identifier:{identifier}.png")
                    cv2.imwrite(f'{CAR_IMAGE_FOLDER}/{car_image_filename}', car_crop)
                    # cv2.imwrite(f'{CAR_IMAGE_FOLDER}/{car_image_filename}', license_plate_crop_thresh)
                    # cv2.imwrite(car_image_filename, car_crop)

                license_plate_image_filename = temp_filename

                cv2.imwrite(
                    f'{DETECTION_IMAGE_FOLDER}/{license_plate_image_filename}', license_plate_crop)

                temp_result_dict = {'raw_license_plate_text': license_plate_text,
                                    'car_img_filename': car_image_filename, 'frame_img_filename': frame_image_filename,
                                    'license_plate_img_filename': license_plate_image_filename,
                                    'license_plate_text_score':license_plate_text_score
                                    }

                logging.info(
                    f'Plat kendaraan terekognisi: {license_plate_text}')
                detection_list.append(temp_result_dict)

    return detection_list, detected_car_history


def detect_plate_on_sent_image(image, temp_img_path, temp_image_name=None, detect_type= "kamera", loc=None):
    # detect_type= "kamera" | "manual"
    detected_car_history= np.array([])
    result_list= []

    if temp_image_name is None:
        temp_image_name= temp_img_path

    start_time = time.time()
    logging.info(f'Memulai deteksi ({detect_type}) plat kendaraan pada {temp_image_name} ...')
    
    # result_list = oevlpr_detection(image, filename=temp_img_path, count_runtime=True)
    temp_result_list, temp_detected_car_history = oevlpr_detection(image, filename=temp_img_path, upscale_amount=10, vertical_stretch=0.75, apply_remove_noise=False, apply_straightened_twice=True, apply_bitwise_not=True, apply_opening=True, thresholding_type=1)

    if len(temp_result_list)>0:
      result_list+=temp_result_list

      if temp_detected_car_history.size>0:
        detected_car_history= np.array(temp_detected_car_history) if detected_car_history.size == 0 else np.concatenate((detected_car_history, temp_detected_car_history))

        
    for idx, result_dict in enumerate(result_list):
        raw_license_plate_text = result_dict['raw_license_plate_text']
        validated_raw_plate_text = validate_raw_plate_text(raw_license_plate_text, loc)

        logging.info(
                    f'Plat kendaraan {raw_license_plate_text} telah divalidasi menjadi {validated_raw_plate_text}')

        plate_num = get_license_plate_num(validated_raw_plate_text)
        plate_type = get_plate_type(plate_num)
        is_violating = get_is_car_violating(plate_num)

        print('license_plate_text_score',result_dict['license_plate_text_score'])

        result_dict['index'] = idx
        result_dict['fullPlateNumber'] = validated_raw_plate_text
        result_dict['plateNumber'] = plate_num
        result_dict['plateType'] = plate_type
        result_dict['policyAtTheMoment'] = check_todays_policy()
        result_dict['isViolating'] = is_violating
        result_dict['detectionDate'] = get_current_date()
        result_dict['detectionTime'] = get_current_time()
        result_dict['imagePath'] = result_dict['license_plate_img_filename']
        result_dict['carImagePath'] = result_dict['car_img_filename']
        result_dict['frameImagePath'] = result_dict['frame_img_filename']
        

        # print('result_dict:', result_dict)

    end_time = time.time()
    running_time= end_time-start_time

    logging.info(f'Deteksi {temp_image_name} berjalan selama {running_time:.2f} detik')
    logging.info(f'Deteksi {temp_image_name} selesai.')

    return result_list


def get_dummy_detection(image_data, image_name):
    save_image_cv(image_data, image_name, DETECTION_IMAGE_FOLDER)
    save_image_cv(image_data, image_name, CAR_IMAGE_FOLDER)
    save_image_cv(image_data, image_name, FRAME_IMAGE_FOLDER)

    detection_data = {
        "fullPlateNumber": "AB 1280 TT",
        "plateNumber": 1280,
        "isViolating": False,
        "plateType": "genap",
        "policyAtTheMoment": "genap",
        "detectionDate": get_current_date(),
        "detectionTime": get_current_time(),
        "detector_id": 1,
        "imagePath": f'{image_name}',
        "carImagePath": f'{image_name}',
        "frameImagePath": f'{image_name}',
    }

    return detection_data
