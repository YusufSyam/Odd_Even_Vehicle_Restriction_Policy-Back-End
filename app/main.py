from fastapi import FastAPI, Path, Header, Body
from app.api.models.detector import *

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_db():
    init_db(app)

@app.get('/')
def index():
    return {"key": "Hello World"}

@app.post('/detector')
async def add_detector(detector_info:detector_pydantic_in):
    detector_obj= await Detector.create(**detector_info.dict(exclude_unset=True))
    response= await detector_pydantic.from_tortoise_orm(detector_obj)

    return {
        "status":"ok",
        "data": response
    }

@app .get('/detector/all')
async def get_detector_all():
    response= await detector_pydantic.from_queryset(Detector.all())

    return {
        "status":"ok",
        "data": response
    }

@app.get('/detector/{detector_id}')
async def get_detector_spesific(detector_id: int):
    response= await detector_pydantic.from_queryset_single(Detector.get(id=detector_id))

    return {
        "status":"ok",
        "data": response
    }

@app.put('/detector/{detector_id}')
async def update_detector(detector_id: int, update_info: detector_pydantic_in):
    detector= await Detector.get(id=detector_id)
    update_info= update_info.dict(exclude_unset=True)

    detector.city= update_info['city']
    detector.roadName= update_info['roadName']
    detector.province= update_info['province']
    detector.subDistrict= update_info['subDistrict']
    detector.ward= update_info['ward']
    detector.roadImagePath= update_info['roadImagePath']
    detector.description= update_info['description']

    await detector.save()

    response= await detector_pydantic.from_tortoise_orm(detector)

    return {
        "status":"ok",
        "data": response
    }

@app.get('/detector/card/all')
async def get_detector_card_all():
    data= await detector_pydantic.from_queryset(Detector.all())

    new_data= []

    for i in data:
        temp_obj= {
            "id": i.id,
            "roadName": i.roadName,
            "province": i.province,
            "city": i.city,
            "status": "Aktif",
            "detectedViolatorTotal": 53*int(i.id)-int(i.id),
            "passingVehicleTotal": 149  *int(i.id),
            "trafficConditions": "Macet",
            "notification": 0,
        }
        
        new_data.append(temp_obj)

    return {
        "status":"ok",
        "data": new_data
    }
