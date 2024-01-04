# Pydantic
from pydantic import BaseModel


class CompanyData(BaseModel):
    manage: str


class CompanyInDB(BaseModel):
    id: str | None = None
    name: str
    data: CompanyData
