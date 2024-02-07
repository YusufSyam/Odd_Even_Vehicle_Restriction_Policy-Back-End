from app.utils.functions.date import parse_date_detection, get_current_date, get_current_time
from app.utils.functions.file import delete_image_if_exists, decode_and_save_image, save_image, save_image_cv

from app.utils.const.directory import DETECTION_IMAGE_FOLDER, TEMPORARY_IMAGE_FOLDER, DETECTION_IMAGE_FOLDER, PLATE_IMAGE_FOLDER, FRAME_IMAGE_FOLDER

def get_dummy_detection(image_data, image_name):
    save_image_cv(image_data, image_name, DETECTION_IMAGE_FOLDER)
    save_image_cv(image_data, image_name, PLATE_IMAGE_FOLDER)
    save_image_cv(image_data, image_name, FRAME_IMAGE_FOLDER)

    detection_data = {
        "fullPlateNumber": "AB 1280 TT",
        "plateNumber": 1280,
        "isViolating": False,
        "plateType": "genap",
        "policyAtTheMoment": "genap",
        "detectionDate": get_current_date(),
        "detectionTime": get_current_time(),
        "detector_id":1,
        "imagePath": f'{image_name}',
        "plateImagePath": f'{image_name}',
        "frameImagePath": f'{image_name}',
    }

    return detection_data
