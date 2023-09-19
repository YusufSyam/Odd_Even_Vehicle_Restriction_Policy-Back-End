import uuid

def get_unique_image_name(road_name):
  return f'{road_name}_{str(uuid.uuid4())}.png'
