# Pydantic
from pydantic import BaseModel


class QueryFrameSchema(BaseModel):
    key: str
    value: str
    link: str

    class Config:
        extra="allow"

    def extra_fields(self):
        # Obtener los nombres de los campos definidos en el modelo
        defined_fields = set(self.__annotations__.keys())
        # Obtener los campos realmente establecidos en la instancia
        all_fields = set(self.model_fields_set)
        # Calcular los campos adicionales como la diferencia
        additional_fields = all_fields - defined_fields
        # Devolver los campos adicionales y sus valores
        return {field: getattr(self, field) for field in additional_fields}