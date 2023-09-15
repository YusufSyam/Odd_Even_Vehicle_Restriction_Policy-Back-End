from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from typing import Optional

from .detector_model import Detector

class Detection(Model):
    id= fields.IntField(pk=True)
    detector= fields.ForeignKeyField('models.Detector', related_name='detector', nullable=False)
    fullPlateNumber= fields.CharField(max_length=20, nullable=False)
    timeDetected= fields.DatetimeField()
    plateNumber= fields.IntField(max_length=10, nullable=False)
    imagePath= fields.TextField()
    isViolating= fields.BooleanField(nullable=False)
    plateType= fields.CharField(max_length=10, nullable=False)
    policyAtTheMoment= fields.CharField(max_length=10, nullable=False)

  
detection_pydantic= pydantic_model_creator(Detection, name="Detection")
detection_pydantic_in= pydantic_model_creator(Detection, name="DetectionIn", exclude_readonly= True, exclude=['timeDetected'])