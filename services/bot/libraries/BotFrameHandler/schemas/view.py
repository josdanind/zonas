# Standard Library
from uuid import UUID

# Pydantic
from pydantic import BaseModel


class ViewSchema(BaseModel):
    id_container_main: UUID
