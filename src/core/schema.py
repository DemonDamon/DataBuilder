from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class FieldType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"


@dataclass
class Field:
    name: str
    type: FieldType
    choices: List[Any] = None
    required: bool = True


class Schema:
    def __init__(self, fields: List[Dict[str, Any]]):
        self.fields = [Field(**field) for field in fields]
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """验证数据是否符合schema定义"""
        for field in self.fields:
            if field.name not in data and field.required:
                return False
            if field.name in data:
                value = data[field.name]
                if field.choices and value not in field.choices:
                    return False
        return True
