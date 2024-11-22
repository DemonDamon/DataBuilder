from typing import List, Dict, Any
from .schema import Schema


class DataValidator:
    def __init__(self, schema: Schema):
        self.schema = schema
    
    def validate_item(self, item: Dict[str, Any]) -> bool:
        """验证单条数据"""
        return self.schema.validate(item)
    
    def validate_batch(self, items: List[Dict[str, Any]]) -> List[bool]:
        """验证一批数据"""
        return [self.validate_item(item) for item in items]
    
    def filter_valid_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤出有效的数据项"""
        return [item for item in items if self.validate_item(item)]
