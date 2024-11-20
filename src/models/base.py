from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseModel(ABC):
    """大模型基类，定义基本接口"""
    
    @abstractmethod
    def __init__(self, model_config: Dict[str, Any]):
        """初始化模型"""
        self.config = model_config
    
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """生成回复"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        pass