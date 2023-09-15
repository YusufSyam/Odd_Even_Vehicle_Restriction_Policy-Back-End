from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from typing import Optional

class Detection(Model):
    id= fields.IntField(pk=True)
    detector= fields.ForeignKeyField('models.Detector', related_name='detector', nullable=False)
    plateNumber= fields.IntField(max_length=10, nullable=False)
    timeDetected= fields.DatetimeField()
    details = fields.ForeignKeyField('models.DetectionDetails', related_name='detection_details', nullable=False)

  
detection_pydantic= pydantic_model_creator(Detection, name="Detection")
detection_pydantic_in= pydantic_model_creator(Detection, name="DetectionIn", exclude_readonly= True)