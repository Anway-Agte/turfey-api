from pydantic import BaseModel, Field
from datetime import datetime


class Booking(BaseModel):
    user_id: str = Field(...)
    turf_id: str = Field(...)
    start_time: int = Field(gt=0, lt=24)
    end_time: int = Field(gt=0, le=24)
    day: int = Field(..., gt=0, le=31)
    month: int = Field(..., gt=0, le=12)
    year: int = Field(..., ge=2021)
