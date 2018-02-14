# -*- coding: utf-8 -*-
from jsonschema import validate

minyans_schema = {
    "type": "array",
    "required": ["name", "time", "day"],
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "time": {"type": "string"},
        "day": {"type": "string"}
    }
}

geo_schema = {
    "type": "object",
    "required": ["lat", "lon"],
    "additionalProperties": False,
    "properties": {
        "lat": {"type": "number"},
        "lon": {"type": "number"}
    }
}

synagouge_schema = {
    "type": "object",
    "required": ["name", "geo"],
    "additionalProperties": False,
    "properties": {
        "address": {"type": "string"},
        "comments": {"type": "string"},
        "name": {"type": "string"},
        "nosach": {"type": "string"},
        "geo": geo_schema,
        "classes": {"type": "boolean"},
        "parking": {"type": "boolean"},
        "sefer-tora": {"type": "boolean"},
        "wheelchair-accessible": {"type": "boolean"},
        "minyans": minyans_schema
    }
}


def validate_synagogues(synagouge):
    validate(synagouge, synagouge_schema)
