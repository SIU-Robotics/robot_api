import json
import jsonschema
from jsonschema import validate


class Validation:

    command_schema = {
        "type": "object",
        "properties": {
            "type": {"type", "string"},
            "direction": {"type", "string"},
            "speed": {"type", "number"},
        },
    }

    def __init__(self, json_obj):
        self.json = json_obj

    def validate_json(self):
        try:
            validate(instance=self.json, schema=self.command_schema)
        except jsonschema.exceptions.ValidationError as e:
            return False
        return True
