from typing import List, Dict, Any
import asyncio
from ..models.base import BaseModel
from ..models.openai import OpenAIModel
from ..models.llama import LlamaModel
from .schema import Schema
from .validator import DataValidator
from ..utils.helpers import create_prompt, save_json_data

class DataBuilder:
    def __init__(self, task_config: Dict[str, Any], model_config: Dict[str, Any]):
        self.task_config = task_config
        self.model_config = model_config
        self.schema = Schema(task_config['schema']['fields'])
        self.validator = DataValidator(self.schema)
        self.model = self._init_model()
    
    def _init_model(self) -> BaseModel:
        """初始化模型"""
        model_type = self.model_config['type'].lower()
        if model_type == 'openai':
            return OpenAIModel(self.model_config)
        elif model_type == 'llama':
            return LlamaModel(self.model_config)
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")
    
    async def generate_batch(self, batch_size: int) -> List[Dict[str, Any]]:
        """生成一批数据"""
        prompt = create_prompt(
            self.task_config['description'],
            self.task_config['examples']
        )
        
        response = await self.model.generate(prompt)
        # 这里需要解析模型返回的文本，转换为结构化数据
        # 具体实现取决于模型输出格式
        
        # 验证并过滤数据
        valid_data = self.validator.filter_valid_items(response)
        return valid_data[:batch_size]
    
    async def generate_dataset(self, total_samples: int, batch_size: int = 10) -> List[Dict[str, Any]]:
        """生成完整数据集"""
        dataset = []
        while len(dataset) < total_samples:
            batch = await self.generate_batch(batch_size)
            dataset.extend(batch)
        return dataset[:total_samples]
    
    def save_dataset(self, data: List[Dict[str, Any]], output_path: str):
        """保存数据集"""
        save_json_data(data, output_path)
    
    async def validate_generation(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """验证生成的数据质量"""
        metrics = {
            "total": len(data),
            "valid": 0,
            "invalid": 0,
            "validation_errors": []
        }
        
        valid_data = []
        for item in data:
            try:
                if self.validator.is_valid(item):
                    valid_data.append(item)
                    metrics["valid"] += 1
                else:
                    metrics["invalid"] += 1
                    metrics["validation_errors"].append(
                        self.validator.get_error_messages(item)
                    )
            except Exception as e:
                metrics["invalid"] += 1
                metrics["validation_errors"].append(str(e))
        
        return {
            "data": valid_data,
            "metrics": metrics
        }