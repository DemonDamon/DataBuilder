from typing import Dict, List, Any
import pandas as pd
from .base import BaseSkill


class ClassificationSkill(BaseSkill):
    def __init__(
        self,
        name: str,
        instructions: str,
        labels: Dict[str, List[str]],
        input_template: str,
        output_template: str
    ):
        super().__init__(
            name=name,
            instructions=instructions,
            input_template=input_template,
            output_template=output_template,
            labels=labels
        )
        
    async def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        """应用分类技能"""
        # 在运行时中实现具体的分类逻辑
        return data

    @staticmethod
    def evaluate_predictions(predictions: pd.Series, ground_truth: pd.Series) -> float:
        """评估预测结果
        Args:
            predictions: 预测结果Series
            ground_truth: 真实标签Series
        Returns:
            float: 准确率
        """
        # 从预测结果中提取标签
        pred_labels = predictions.apply(
            lambda x: x.split(':')[-1].strip()
            if ':' in str(x) else str(x).strip()
        )
        # 计算准确率
        return (pred_labels == ground_truth).mean()

    def process_predictions(self, predictions: pd.DataFrame) -> pd.DataFrame:
        """处理预测结果格式
        Args:
            predictions: 原始预测结果
        Returns:
            pd.DataFrame: 处理后的预测结果
        """
        output_col = list(self.labels.keys())[0]
        predictions[output_col] = predictions[output_col].apply(
            lambda x: x.split(':')[-1].strip()
            if ':' in str(x) else str(x).strip()
        )
        return predictions
