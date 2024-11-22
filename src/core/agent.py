from typing import Dict, Any, Optional, Union
import pandas as pd
from src.skills.base import BaseSkill
from src.environments.base import BaseEnvironment
from src.runtimes.base import BaseRuntime

class Agent:
    def __init__(
        self,
        skills: BaseSkill,
        environment: BaseEnvironment,
        runtimes: Dict[str, BaseRuntime],
        default_runtime: str = 'default'
    ):
        self.skills = skills
        self.environment = environment
        self.runtimes = runtimes
        self.default_runtime = default_runtime
        self.best_accuracy = 0
        self.best_instructions = None
        self.training_history = []
        
    async def learn(self, learning_iterations: int = 3) -> None:
        """训练模型"""
        runtime = self.runtimes[self.default_runtime]
        train_data = await self.environment.load_data()
        
        for i in range(learning_iterations):
            print(f"\n开始第 {i+1} 轮训练...")
            
            # 进行预测
            raw_predictions = await runtime.run(self.skills, train_data)
            predictions = self.skills.process_predictions(raw_predictions)
            
            # 获取反馈
            feedback = await self.environment.get_feedback(predictions)
            accuracy = list(feedback.values())[0]
            
            print(f"训练准确率: {feedback}")
            
            if accuracy < 1.0:
                old_instructions = self.skills.instructions
                new_instructions = await self._optimize_instructions(accuracy)
                
                # 使用新提示词进行测试
                self.skills.instructions = new_instructions
                test_raw_predictions = await runtime.run(self.skills, train_data)
                test_predictions = self.skills.process_predictions(test_raw_predictions)
                test_feedback = await self.environment.get_feedback(test_predictions)
                test_accuracy = list(test_feedback.values())[0]
                
                # 只有当新提示词效果更好时才保留
                if test_accuracy > accuracy:
                    print(f"新提示词效果更好: {test_accuracy} > {accuracy}")
                    self.best_accuracy = test_accuracy
                    self.best_instructions = new_instructions
                else:
                    print(f"保留原提示词: {test_accuracy} <= {accuracy}")
                    self.skills.instructions = old_instructions
    
    async def _optimize_instructions(self, accuracy: float) -> str:
        """优化提示词"""
        runtime = self.runtimes[self.default_runtime]
        
        # 获取技能的配置信息
        skill_config = {
            'labels': self.skills.labels,
            'input_template': self.skills.input_template,
            'output_template': self.skills.output_template
        }
        
        # 构建优化提示
        optimization_prompt = f"""
## 当前配置
- 提示词: {self.skills.instructions}
- 输入模板: {skill_config['input_template']}
- 输出模板: {skill_config['output_template']}
- 可用标签: {skill_config['labels']}

## 训练数据示例
{self._format_training_history()}

## 训练准确率
{accuracy}

## 优化要求
1. 提示词必须明确指出使用输入模板和输出模板的格式
2. 强调只能使用预定义的标签
3. 禁止添加任何额外解释或描述
4. 保持提示词简洁清晰

请直接返回优化后的提示词，不要包含任何解释。
"""
        
        # 获取优化建议
        new_instructions = await runtime.run_raw(optimization_prompt)
        return new_instructions.strip()

    def get_optimized_prompt(self) -> str:
        """获取最佳提示词"""
        return self.best_instructions or self.skills.instructions
        
    async def run(self, data: pd.DataFrame) -> pd.DataFrame:
        """预测新数据"""
        runtime = self.runtimes[self.default_runtime]
        return await runtime.run(self.skills, data)

    def _validate_predictions(self, predictions: pd.DataFrame) -> bool:
        """验证预测结果格式"""
        # 获取输出列名
        output_column = list(self.skills.labels.keys())[0]
        output_template = self.skills.output_template
        valid_labels = self.skills.labels[output_column]
        
        # 从输出模板中提取前缀
        prefix = output_template.split('{')[0].strip()
        
        for pred in predictions[output_column]:
            # 检查是否符合输出模板格式
            if not pred.startswith(prefix):
                return False
            # 检查是否使用了有效标签
            label = pred.replace(prefix, '').strip()
            if label not in valid_labels:
                return False
        return True

    def _format_training_history(self) -> str:
        """格式化训练历史数据"""
        if not self.training_history:
            return "暂无训练历史"
        
        formatted_history = []
        for record in self.training_history:
            formatted_history.append(f"""
### 迭代 {record['iteration']}
- 提示: {record['instructions']}
- 准确率: {record['accuracy']}
- 预测结果:
{record['predictions'].to_string()}
""")
        
        return "\n".join(formatted_history)