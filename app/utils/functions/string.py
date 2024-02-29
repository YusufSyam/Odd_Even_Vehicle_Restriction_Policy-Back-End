import uuid
import re

from app.utils.const.const import SENT_IMAGE_DETECTOR_DELIMITER

def get_unique_image_name(image_name):
  return f'{image_name}_{str(uuid.uuid4())}.png'

def generate_unique_string():
  unique_string = str(uuid.uuid4())
  return unique_string

def get_detector_id(string, delimiter=None):
  if delimiter is None:
    delimiter= SENT_IMAGE_DETECTOR_DELIMITER

  pattern = re.compile(fr'{re.escape(delimiter)}(\d+)')
  hasil = re.search(pattern, string)
  
  if hasil:
    angka_setelah_tanda_pagar = hasil.group(1)
    return int(angka_setelah_tanda_pagar)
  else:
    return -1


def decode_sent_image(input_string):
  input_string = input_string.replace(".png", "").replace(".jpg", "")

  substrings = input_string.split(SENT_IMAGE_DETECTOR_DELIMITER)
  result_dict = {}

  for substring in substrings:
    try:
      key, value = substring.split(":", 1)
      result_dict[key] = value
    except:
      continue

  return result_dict
