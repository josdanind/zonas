# Pydantic
from pydantic import BaseModel


class CropWorkerInDB(BaseModel):
    id: int | None = None
    crop_id: int
    worker_id: int
