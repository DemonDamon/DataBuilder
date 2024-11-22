from typing import Dict, Any
from abc import ABC, abstractmethod
from typing import Dict, List, Any
import pandas as pd

class BaseSkill(ABC):
    def __init__(
        self,
        name: str,
        instructions: str,
        input_template: str,
        output_template: str,
        labels: Dict[str, List[str]]
    ):
        self.name = name
        self.instructions = instructions
        self.input_template = input_template
        self.output_template = output_template
        self.labels = labels
        self.metrics = {}
    
    @abstractmethod
    async def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        """应用技能到数据"""
        pass
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取技能执行指标"""
        return self.metrics