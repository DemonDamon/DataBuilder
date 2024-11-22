from typing import Any

class RuntimeManager:
    def __init__(self):
        self.runtimes = {}
        self.current_runtime = None
    
    def register_runtime(self, name: str, runtime: Any):
        """注册新的运行时"""
        self.runtimes[name] = runtime
    
    def switch_runtime(self, name: str):
        """切换运行时"""
        if name not in self.runtimes:
            raise ValueError(f"Runtime {name} not found")
        self.current_runtime = self.runtimes[name]