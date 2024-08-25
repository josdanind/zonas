from pydantic import BaseModel, create_model


def make_schema_fields_optional(model: BaseModel, remove_field: str | None = None) -> BaseModel:
    fields = {
        name: (field.annotation | None, None)
        for name, field in model.model_fields.items()
        if name != remove_field
    }

    return create_model(f"{model.__name__}Update", **fields)

