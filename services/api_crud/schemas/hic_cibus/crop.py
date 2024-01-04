# Standard Library
from datetime import date

# Pydantic
from pydantic import BaseModel


class CropData(BaseModel):
    zone: str
    pilot: bool
    irrigation_system: dict


class CropInDB(BaseModel):
    id: int | None = None
    farm_id: int
    crop: str
    crop_plot: str
    is_active: bool
    seedtime: date
    harvest_dates: list[date]
    end_of_crop: date | None = None
    location: dict
    categories: list[str]
    varieties: dict
    data: CropData
