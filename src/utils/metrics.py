from typing import Dict, Any, Optional
from datetime import datetime
import logging
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class MetricsData(BaseModel):
    """指标数据模型"""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_samples: int = 0
    valid_samples: int = 0
    invalid_samples: int = 0
    error_types: Dict[str, int] = {}
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class MetricsCollector:
    def __init__(self):
        self.metrics = {
            "generation": MetricsData(),
            "validation": MetricsData(),
            "runtime": MetricsData(),
            "skills": {}  # 用于存储不同技能的指标
        }
        self.start_time = datetime.now()
    
    def start_tracking(self, category: str, skill_name: Optional[str] = None):
        """开始追踪某个类别的指标"""
        target = self._get_target(category, skill_name)
        target.start_time = datetime.now()
    
    def stop_tracking(self, category: str, skill_name: Optional[str] = None):
        """停止追踪某个类别的指标"""
        target = self._get_target(category, skill_name)
        target.end_time = datetime.now()
    
    def update(self, category: str, values: Dict[str, Any], skill_name: Optional[str] = None):
        """更新指标"""
        try:
            target = self._get_target(category, skill_name)
            for key, value in values.items():
                if hasattr(target, key):
                    setattr(target, key, value)
            logger.debug(f"Updated metrics for {category}: {values}")
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
    
    def _get_target(self, category: str, skill_name: Optional[str] = None) -> MetricsData:
        """获取目标指标对象"""
        if skill_name:
            if skill_name not in self.metrics["skills"]:
                self.metrics["skills"][skill_name] = MetricsData()
            return self.metrics["skills"][skill_name]
        return self.metrics[category]
    
    def get_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        runtime = (datetime.now() - self.start_time).total_seconds()
        return {
            "runtime_seconds": runtime,
            "metrics": {
                k: v.dict() if isinstance(v, MetricsData) else v
                for k, v in self.metrics.items()
            }
        }
