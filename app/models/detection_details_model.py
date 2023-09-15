from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from typing import Optional

class DetectionDetails(Model):
    id= fields.IntField(pk=True)
    fullPlateNumber= fields.CharField(max_length=20, nullable=False)
    imagePath= fields.CharField(max_length=1000, nullable=False)
    isViolating= fields.BooleanField(nullable=False)
    plateType= fields.CharField(max_length=10, nullable=False)
    policyAtTheMoment= fields.CharField(max_length=10, nullable=False)


detection_details_pydantic= pydantic_model_creator(DetectionDetails, name="DetectionDetails")
detection_details_pydantic_in= pydantic_model_creator(DetectionDetails, name="DetectionDetailsIn", exclude_readonly= True)