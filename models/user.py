from pydantic import BaseModel, Field


class User(BaseModel):
    fname: str = Field(...)
    lname: str = Field(...)
    mobile: str = Field(max_length=10)
    pincode: str = Field(max_length=6)
    city: str = Field(...)
