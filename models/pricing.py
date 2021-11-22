from pydantic import BaseModel, Field


class Pricing(BaseModel):
    day: str = Field(...)
    start_time: int = Field(ge=6)
    end_time: int = Field(le=24)
    cost: float = Field(...)
