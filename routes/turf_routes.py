from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from models.index import ErrorModel, ResponseModel
from models.turf import Turf
from models.pricing import Pricing
from config.database import db
from uuid import uuid4
from collections import defaultdict

turf_router = APIRouter()


@turf_router.get("/")
async def get_all_turfs():
    turfs = list(db.turfs.find({}, {"_id": 0}))
    return ResponseModel(turfs)


@turf_router.post("/")
async def create_turf(turf: Turf):
    turf = jsonable_encoder(turf)
    turf["turf_id"] = str(uuid4())
    if db.turfs.insert_one(turf):
        created_turf = db.turfs.find_one({"turf_id": turf["turf_id"]}, {"_id": 0})
        if created_turf:
            return ResponseModel(data=created_turf)
        else:
            return ErrorModel(
                message="There was an error in creating your turf, please try again"
            )
    else:
        return ErrorModel(message="Oops! Please try again")


@turf_router.get("/{turf_id}")
async def get_turf(turf_id: str):
    turf = db.turfs.find_one({"turf_id": turf_id}, {"_id": 0})
    if turf:
        return ResponseModel(turf)
    else:
        return ErrorModel({}, "Oops! There was an error, please try again!")


@turf_router.get("/pricing/{turf_id}")
async def get_pricing(turf_id: str):
    turf = db.turfs.find_one({"turf_id": turf_id}, {"_id": 0})
    slots = turf["slots"]
    res = {}
    for item in slots:
        res.setdefault(item["day"], []).append(item)
    weekday = res["Weekday"]
    amount = 0
    weekday_slots = {"cost": 0, "timings": []}
    weekday_result = []
    for day in weekday:
        print(amount)
        print(day["cost"])
        if day["cost"] != amount:
            if weekday_slots["cost"] != 0:
                print(weekday_slots)
                weekday_result.append(weekday_slots)
                weekday_slots = {"cost": 0, "timings": []}
                amount = 0
            amount = day["cost"]
            weekday_slots["cost"] = amount
            weekday_slots["timings"].append(day["time"])
        else:
            weekday_slots["timings"].append(day["time"])
    weekday_result.append(weekday_slots)
    weekend = res["Weekend"]
    amount = 0
    weekend_slots = {"cost": 0, "timings": []}
    weekend_result = []
    for day in weekend:
        print(amount)
        print(day["cost"])
        if day["cost"] != amount:
            if weekend_slots["cost"] != 0:
                print(weekend_slots)
                weekend_result.append(weekend_slots)
                weekend_slots = {"cost": 0, "timings": []}
                amount = 0
            amount = day["cost"]
            weekend_slots["cost"] = amount
            weekend_slots["timings"].append(day["time"])
        else:
            weekend_slots["timings"].append(day["time"])
    weekend_result.append(weekend_slots)
    return {
        "data": {"weekday": weekday_result, "weekend": weekend_result},
        "success": True,
    }


@turf_router.put("/pricing")
async def add_pricing(pricing: Pricing, turf_id: str):
    if db.turfs.find_one({"turf_id": turf_id}, {"_id": 0}):
        for time in range(pricing.start_time, pricing.end_time):
            slot = {"day": pricing.day, "time": time, "cost": pricing.cost}
            db.turfs.update_one({"turf_id": turf_id}, {"$push": {"slots": slot}})
        return db.turfs.find_one({"turf_id": turf_id}, {"_id": 0})
    else:
        return ErrorModel(message="This turf does not exist")
