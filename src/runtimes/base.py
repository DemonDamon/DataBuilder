from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
from src.skills.base import BaseSkill


class BaseRuntime(ABC):
    @abstractmethod
    async def run(
        self,
        skill: BaseSkill,
        data: pd.DataFrame
    ) -> pd.DataFrame:
        """运行技能"""
        pass
