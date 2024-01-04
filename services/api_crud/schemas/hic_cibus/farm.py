# Pydantic
from pydantic import BaseModel


class FarmData(BaseModel):
    city: str
    hamlet: str


class FarmInDB(BaseModel):
    id: int | None = None
    company_id: int
    name: str
    location: dict
    data: FarmData
