from typing import Dict, Any, List, Optional
import pandas as pd
from openai import OpenAI
from .base import BaseRuntime
from src.skills.base import BaseSkill

class OpenAIRuntime(BaseRuntime):
    def __init__(
        self,
        model: str,
        base_url: str,
        api_key: str,
        temperature: float = 0.7,
        timeout: int = 30
    ):
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout
        )

    async def run(
        self,
        skill: BaseSkill,
        data: pd.DataFrame
    ) -> pd.DataFrame:
        """运行技能"""
        results = []
        for _, row in data.iterrows():
            # 构建输入
            input_text = skill.input_template.format(**row.to_dict())
            
            try:
                # 调用 OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": skill.instructions},
                        {"role": "user", "content": input_text}
                    ],
                    temperature=self.temperature,
                    timeout=self.timeout
                )
                
                # 解析输出
                output = response.choices[0].message.content
                results.append(output)
                
            except Exception as e:
                print(f"API 调用出错: {str(e)}")
                results.append("错误")
                
        # 构建结果 DataFrame
        predictions = pd.DataFrame(results, columns=[skill.name])
        return predictions

    async def run_raw(self, prompt: str) -> str:
        """直接运行原始提示词"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API 调用出错: {str(e)}")
            return ""