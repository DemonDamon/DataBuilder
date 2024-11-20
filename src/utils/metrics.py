class MetricsCollector:
    def __init__(self):
        self.metrics = {
            "generation": {
                "total_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "total_samples": 0,
                "valid_samples": 0,
                "invalid_samples": 0
            },
            "validation": {
                "error_types": {},
                "field_errors": {}
            },
            "runtime": {
                "total_time": 0,
                "average_time": 0
            }
        }
    
    def update(self, metric_type: str, values: Dict[str, Any]):
        """更新指标"""
        if metric_type in self.metrics:
            self.metrics[metric_type].update(values)