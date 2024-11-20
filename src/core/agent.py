from typing import Dict, Any, List
from .builder import DataBuilder

class Agent:
    def __init__(self, task_config: Dict[str, Any], model_config: Dict[str, Any]):
        self.builder = DataBuilder(task_config, model_config)
        self.memory = []  # 存储生成历史
        self.metrics = {}  # 存储指标
    
    async def generate_with_feedback(self, batch_size: int, feedback_func=None):
        """带反馈的数据生成"""
        data = await self.builder.generate_batch(batch_size)
        if feedback_func:
            data = feedback_func(data)
        self.memory.extend(data)
        return data
    
    def get_metrics(self):
        """获取生成指标"""
        return self.metrics