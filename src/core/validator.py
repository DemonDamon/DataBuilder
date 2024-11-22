from typing import List, Dict, Any
from .schema import Schema


class DataValidator:
    def __init__(self, schema: Schema):
        self.schema = schema
    
    def is_valid(self, data: Dict[str, Any]) -> bool:
        for field in self.schema.fields:
            if field.name not in data:
                return False
            if not self.schema.validate_field(field.name, data[field.name]):
                return False
        return True
    
    def filter_valid_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [item for item in items if self.is_valid(item)]
