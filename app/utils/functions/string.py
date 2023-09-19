import uuid

def get_unique_image_name(image_name):
  return f'{image_name}_{str(uuid.uuid4())}.png'
