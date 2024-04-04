# Standard Lirary
from pathlib import Path
from uuid import UUID, uuid4

# Pydantic
from pydantic import BaseModel


class ContainerSchema(BaseModel):
    id: UUID = uuid4()
    endpoint_path: str
