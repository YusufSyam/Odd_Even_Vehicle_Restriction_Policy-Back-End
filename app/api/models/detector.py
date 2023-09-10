from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from typing import Optional

class Detector(Model):
    id= fields.IntField(pk=True)
    roadName= fields.CharField(max_length=200, nullable=False, unique=True)
    province= fields.CharField(max_length=100, nullable=False)
    city= fields.CharField(max_length=100, nullable=False)
    subDistrict= fields.CharField(max_length=100)
    ward= fields.CharField(max_length=100)
    roadImagePath= fields.CharField(max_length=1000)
    description= fields.CharField(max_length=2000)

class DetectorWImage(Model):
    id= fields.IntField(pk=True)
    roadName= fields.CharField(max_length=200, nullable=False, unique=True)
    province= fields.CharField(max_length=100, nullable=False)
    city= fields.CharField(max_length=100, nullable=False)
    subDistrict= fields.CharField(max_length=100)
    ward= fields.CharField(max_length=100)
    description= fields.CharField(max_length=2000)
    # imageBase64= fields.CharField(max_length=4294967294)
    imageBase64= fields.TextField()
    # status= // Later ...

class DetectorIn(BaseModel):
    roadName: str
    province: str
    city: str
    subDistrict: Optional[str] = None
    ward: Optional[str] = None
    roadImagePath: Optional[str] = None
    description: Optional[str] = None
    
class Detection(Model):
    id= fields.IntField(pk=True)
    detector= fields.ForeignKeyField('models.Detector', related_name='detector', nullable=False)
    plateNumber= fields.IntField(max_length=10, nullable=False)
    timeDetected= fields.DatetimeField()
    details = fields.ForeignKeyField('models.DetectionDetails', related_name='detection_details', nullable=False)

class DetectionDetails(Model):
    id= fields.IntField(pk=True)
    fullPlateNumber= fields.CharField(max_length=20, nullable=False)
    imagePath= fields.CharField(max_length=1000, nullable=False)
    isViolating= fields.BooleanField(nullable=False)
    plateType= fields.CharField(max_length=10, nullable=False)
    policyAtTheMoment= fields.CharField(max_length=10, nullable=False)

detector_pydantic= pydantic_model_creator(Detector, name="Detector")
detection_pydantic= pydantic_model_creator(Detection, name="Detection")
detection_details_pydantic= pydantic_model_creator(DetectionDetails, name="DetectionDetails")

detector_pydantic_in= pydantic_model_creator(Detector, name="DetectorIn", exclude_readonly= True)
detector_pydantic_in_wimage= pydantic_model_creator(DetectorWImage, name="DetectorInWImage", exclude_readonly= True)
detection_pydantic_in= pydantic_model_creator(Detection, name="DetectionIn", exclude_readonly= True)
detection_details_pydantic_in= pydantic_model_creator(DetectionDetails, name="DetectionDetailsIn", exclude_readonly= True)

def init_db(app):
    register_tortoise(
        app,
        db_url='mysql://root@127.0.0.1:3306/oevrp',
        modules={'models': ['app.api.models.detector']},
        generate_schemas=True,
        add_exception_handlers=True
    )