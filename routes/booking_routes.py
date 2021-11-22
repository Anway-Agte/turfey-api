from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from pymongo import message
from models.bookings import Booking
from models.index import ErrorModel, ResponseModel
from config.database import db
from datetime import date
from uuid import uuid4

booking_router = APIRouter()


@booking_router.post("/")
async def book_slot(booking: Booking):
    booking = jsonable_encoder(booking)
    amount = 0
    booking_date = date(booking["year"], booking["month"], booking["day"])
    booking_day = booking_date.weekday()
    timings = []
    if booking_day < 5:
        booking["type"] = "Weekday"
    else:
        booking["type"] = "Weekend"
    for time in range(booking["start_time"], booking["end_time"]):
        slot = db.turfs.find_one(
            {"turf_id": booking["turf_id"]},
            {"_id": 0, "slots": {"$elemMatch": {"day": booking["type"], "time": time}}},
        )
        print(slot)
        amount += slot["slots"][0]["cost"]
        timings.append(time)
    booking["amount"] = amount
    booking["timings"] = timings
    booking["booking_id"] = str(uuid4())
    booking["paid"] = False
    del booking["start_time"]
    del booking["end_time"]
    if db.bookings.insert_one(booking):
        return ResponseModel({}, message="Your slots have been booked successfully")
    return ErrorModel(message="Oops! There was an error, please try again")


@booking_router.get("/slots")
async def get_booked_slots(year: int, month: int, day: int, turf_id: str):
    bookings = list(
        db.bookings.find({"year": year, "month": month, "day": day, "turf_id": turf_id})
    )
    slots = []
    for booking in bookings:
        print(booking)
        slots.extend(booking["timings"])
    return ResponseModel(data={"slots": sorted(slots)})


@booking_router.get("/slot")
async def get_slot(booking_id: str):
    slot = db.bookings.find_one({"booking_id": booking_id}, {"_id": 0})
    if slot:
        return ResponseModel(slot)
    else:
        return ErrorModel(message="Oops, seems like this booking doesn't exist")


@booking_router.get("/user")
async def get_slot(user_id: str):
    slots = list(db.bookings.find({"user_id": user_id}, {"_id": 0}))
    if slots:
        return ResponseModel(slots)
    else:
        return ErrorModel(message="Oops, seems like this booking doesn't exist")


@booking_router.get("/turf")
async def get_slot(turf_id: str):
    slots = list(db.bookings.find({"turf_id": turf_id}, {"_id": 0}))
    if slots:
        return ResponseModel(slots)
    else:
        return ErrorModel(message="Oops, seems like this booking doesn't exist")
