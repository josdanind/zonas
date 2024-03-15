# Standard Library
import json

# Schemas
from schemas import ViewSchema


def set_view_config(config_path: str, cover_path: str) -> ViewSchema:
    with open(config_path, "r") as f:
        config = json.load(f)
        config["cover"] = cover_path

    return ViewSchema(**config)
