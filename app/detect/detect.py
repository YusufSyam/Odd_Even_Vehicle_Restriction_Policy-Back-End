from app.utils.functions.date import parse_date_detection, get_current_date, get_current_time
from app.utils.functions.file import delete_image_if_exists, decode_and_save_image, save_image, save_image_cv

from app.utils.const.directory import DETECTION_IMAGE_FOLDER, TEMPORARY_IMAGE_FOLDER, DETECTION_IMAGE_FOLDER, PLATE_IMAGE_FOLDER, FRAME_IMAGE_FOLDER

from app.detect.detect_const import *

from ultralytics import YOLO
import cv2
import time
import torch



coco_model = YOLO(COCO_MODEL)
license_plate_detector = YOLO(LICENSE_PLATE_MODEL_PATH)

def oevlpr_detection(frame, frame_num=0, count_runtime=False, filename= '', upscale_amount= 6, vertical_stretch= 0.6, opening_kernel_size=(3,3), apply_remove_noise= False, plot= True):
    global coco_model, license_plate_detector
    global TEMP_CAR_IMG_DIR, TEMP_FRAME_IMG_DIR, TEMP_LICENSE_PLATE_IMG_DIR

    # Hapuski ini kalau production mi
    start_time= time.time()

    detections = coco_model(frame, conf= 0.01)[0]
    detected_car = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) == 2:
            detected_car.append([x1, y1, x2, y2, score])

    # print('detected_car', detected_car)

    # Tidak ada mobil yang terdeteksi
    # if len(detected_car)<= 0:
    #     track_ids = []
    # else:
    #     track_ids = mot_tracker.update(np.asarray(detected_car))
    
    track_ids = []
    license_plates = license_plate_detector(frame)[0]

    identifier= filename.split('.')[0]

    is_frame_img_made= False
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        print('IDENTIFIER:', identifier)

        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)
        xcar1, ycar1, xcar2, ycar2 = limit_at_zero(xcar1), limit_at_zero(ycar1), limit_at_zero(xcar2), limit_at_zero(ycar2)

        if True:
        # if car_id != -1:

            # crop car & license plate
            car_crop = frame[int(ycar1):int(ycar2), int(xcar1): int(xcar2), :]
            license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

            # process license plate
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

            license_plate_crop_straight = straightening_image(license_plate_crop_gray)
            license_plate_crop_straight = upscale_image(license_plate_crop_straight, upscale_amount)

            if apply_remove_noise:
                license_plate_crop_straight= remove_noise(license_plate_crop_straight)

            license_plate_crop_thresh = thresholding1(license_plate_crop_straight)
            license_plate_crop_thresh= opening(license_plate_crop_thresh, opening_kernel_size)
            license_plate_crop_thresh= cv2.bitwise_not(license_plate_crop_thresh)
            license_plate_crop_thresh= stretch_vertical(license_plate_crop_thresh, vertical_stretch)
            
            if plot:
              plt.title('license_plate_crop_gray')
              plt.imshow(license_plate_crop_gray, cmap='gray')
              plt.show()

              plt.title('license_plate_crop_thresh')
              plt.imshow(license_plate_crop_thresh, cmap='gray')
              plt.show()
              
            # read license plate number
            license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

            if True:
            # if license_plate_text is not None:
                if not is_frame_img_made:
                    frame_image_filename = os.path.join(TEMP_FRAME_IMG_DIR, f"frame:{frame_num}-identifier:{identifier}.png")
                    cv2.imwrite(frame_image_filename, frame)

                    is_frame_img_made= True

                    if car_id==-1:
                      car_image_filename= None
                    else:
                      car_image_filename = os.path.join(TEMP_CAR_IMG_DIR, f"frame:{frame_num}-car_id:{car_id}-identifier:{identifier}.png")
                      
                try:
                    cv2.imwrite(car_image_filename, car_crop)
                except:
                    print('Car not found')

                license_plate_image_filename = os.path.join(TEMP_LICENSE_PLATE_IMG_DIR,
                            f"frame:{frame_num}-car_id:{car_id}-license_plate-{license_plate_text}-{identifier}.png")
        
                cv2.imwrite(license_plate_image_filename, license_plate_crop)

                license_plate_num= get_license_plate_num(license_plate_text)
                try:
                    is_car_violating= get_is_car_violating(int(license_plate_num))
                except:
                    is_car_violating= None

                temp_result_dict={'raw_license_plate_text':license_plate_text,
                                  'car_img_filename':car_image_filename, 'frame_img_filename':frame_image_filename,
                                  'license_plate_img_filename':license_plate_image_filename,

                                  }
                
                return temp_result_dict

    if count_runtime:
        end_time = time.time()
        print(f'Running Time per Frame: {end_time-start_time}')

    return None


def detect_plate_on_sent_image(image):
  result_dict= oevlpr_detection(image, mot_tracker, filename=temp_img_path)

  print('result_dict:',result_dict)





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
