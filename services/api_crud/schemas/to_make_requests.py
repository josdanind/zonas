# Pydantic
from pydantic import BaseModel


class KeywordsForDB(BaseModel):
    c_name: str
    keywords: list
