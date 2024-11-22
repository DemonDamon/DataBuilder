from typing import Dict, Any
import pandas as pd
from .base import BaseEnvironment, EnvironmentConfig

class StaticEnvironment(BaseEnvironment):
    def __init__(
        self,
        df: pd.DataFrame,
        ground_truth_columns: Dict[str, str]
    ):
        config = EnvironmentConfig(
            df=df,
            ground_truth_columns=ground_truth_columns
        )
        super().__init__(config)
    
    def validate(self, data: pd.DataFrame) -> bool:
        """验证数据格式是否正确"""
        # 检查必要的列是否存在
        if 'text' not in data.columns:
            return False
            
        # 如果是训练数据,检查ground truth列
        if self.config.ground_truth_columns:
            for _, gt_col in self.config.ground_truth_columns.items():
                if gt_col not in data.columns:
                    return False
                    
        return True

    async def load_data(self) -> pd.DataFrame:
        """加载训练数据"""
        return self.config.df
    
    async def get_feedback(self, predictions: pd.DataFrame) -> Dict[str, float]:
        """获取预测反馈
        Args:
            predictions: 预测结果DataFrame
        Returns:
            Dict: 包含准确率等指标
        """
        metrics = {}
        for pred_col, gt_col in self.config.ground_truth_columns.items():
            # 直接比较预测值和真实值
            accuracy = (predictions[pred_col] == self.config.df[gt_col]).mean()
            metrics[f"{pred_col}_accuracy"] = accuracy
        return metrics