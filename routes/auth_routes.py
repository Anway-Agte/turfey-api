from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from models.index import ResponseModel, ErrorModel
from models.user import User
from uuid import uuid4
from config.database import db

auth_router = APIRouter()


@auth_router.post("/")
async def register(user: User = Body(...)):
    user = jsonable_encoder(user)
    user["user_id"] = str(uuid4())
    print(user)
    if db.users.find_one({"mobile": user["mobile"]}):
        return ErrorModel({}, "User with this mobile number already exists")
    else:
        if db.users.insert_one(user):
            created_user = db.users.find_one({"user_id": user["user_id"]}, {"_id": 0})
            if created_user:
                return ResponseModel(created_user, "User registered successfully")
            else:
                return ResponseModel(
                    {}, "There was an error in signing you up, please try again later"
                )
        else:
            return ResponseModel(
                {}, "There was an error in signing you up, please try again later"
            )
