from typing import Dict, Any, List
from abc import ABC, abstractmethod
import pandas as pd
from pydantic import BaseModel, ConfigDict


class EnvironmentConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    df: pd.DataFrame
    ground_truth_columns: Dict[str, str]


class BaseEnvironment(ABC):
    def __init__(self, config: EnvironmentConfig):
        self.config = config
        self.metrics = {}
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """验证数据格式"""
        pass
        
    @abstractmethod
    async def load_data(self) -> pd.DataFrame:
        """加载环境数据"""
        pass
        
    @abstractmethod
    async def get_feedback(self, predictions: Dict[str, Any]) -> Dict[str, float]:
        """获取预测反馈"""
        pass
