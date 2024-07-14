# Pydantic
from pydantic import BaseModel


class QueryFrameSchema(BaseModel):
    key: str
    value: str
    link: str
    farm_id: int
