from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from typing import Optional

class Detector(Model):
    id= fields.IntField(pk=True)
    roadName= fields.CharField(max_length=200, nullable=False, unique=True)
    province= fields.CharField(max_length=100, nullable=False)
    city= fields.CharField(max_length=100, nullable=False)
    subDistrict= fields.CharField(max_length=100)
    ward= fields.CharField(max_length=100)
    roadImagePath= fields.TextField()
    description= fields.CharField(max_length=2000)

detector_pydantic= pydantic_model_creator(Detector, name="Detector")
detector_pydantic_in= pydantic_model_creator(Detector, name="DetectorIn", exclude_readonly= True)

# def init_db(app):
#     register_tortoise(
#         app,
#         db_url='mysql://root@127.0.0.1:3307/oevrp',
#         modules={'models': ['app.models']},
#         generate_schemas=True,
#         add_exception_handlers=True
#     )