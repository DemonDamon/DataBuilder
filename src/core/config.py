from typing import Dict, Any, List
from pydantic import BaseModel, Field

class SchemaField(BaseModel):
    name: str
    type: str
    choices: List[str] = []

class SchemaConfig(BaseModel):
    format: str = "json"
    fields: List[SchemaField]

class TaskConfig(BaseModel):
    description: str
    examples: List[Dict[str, Any]]
    schema: SchemaConfig

class ModelConfig(BaseModel):
    type: str
    name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
