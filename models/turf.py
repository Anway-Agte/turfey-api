from pydantic import BaseModel, Field


class Turf(BaseModel):
    name: str = Field(...)
    addressLine1: str = Field(...)
    addressLine2: str = Field(...)
    contact: str = Field(...)
    slots: list = Field(default=[])
