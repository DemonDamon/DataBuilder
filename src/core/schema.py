from typing import List, Dict, Any
from pydantic import BaseModel


class Field(BaseModel):
    name: str
    type: str
    choices: List[str] = []


class Schema:
    def __init__(self, fields: List[Field]):
        self.fields = fields
    
    def validate_field(self, field_name: str, value: Any) -> bool:
        for field in self.fields:
            if field.name == field_name:
                if field.type == "string":
                    if not isinstance(value, str):
                        return False
                    if field.choices and value not in field.choices:
                        return False
                return True
        return False
