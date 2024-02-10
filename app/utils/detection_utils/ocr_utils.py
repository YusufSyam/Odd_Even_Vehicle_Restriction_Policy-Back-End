import string
import easyocr
# import pytesseract

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=True)

# EASY OCR
def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)

    if detections is None or len(detections) <= 0:
        return 'Tidak ada deteksi', 0

    return ':'.join([i[-2] for i in detections]), 100

