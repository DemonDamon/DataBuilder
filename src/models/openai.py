from typing import Dict, Any, List
import json
from .base import BaseModel
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from ..utils.retry import retry_with_exponential_backoff


# 加载环境变量
env_path = Path('.env')
if not env_path.exists():
    raise FileNotFoundError("未找到 .env 文件，请根据 .env.example 创建配置文件")

load_dotenv(dotenv_path=env_path, override=True)


class OpenAIModel(BaseModel):
    def __init__(self, model_config: Dict[str, Any]):
        super().__init__(model_config)
        # 使用新版本的客户端初始化方式
        self.client = OpenAI(
            base_url=model_config.get('api_base') or os.getenv("OPENAI_API_BASE"),
            api_key=model_config.get('api_key') or os.getenv("OPENAI_API_KEY")
        )
        self.model_name = model_config.get('name', 'gpt-4')
        self.parameters = model_config.get('parameters', {})
    
    async def generate(self, prompt: str) -> List[Dict[str, Any]]:
        @retry_with_exponential_backoff
        async def _generate():
            try:
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{
                        "role": "system",
                        "content": "你是一个数据生成助手。请生成JSON格式的数据，确保每条数据都符合schema定义。"
                                 "生成的数据应该多样化，并且符合实际场景。请直接返回JSON数组，不要包含其他解释文字。"
                    }, {
                        "role": "user",
                        "content": prompt
                    }],
                    **self.parameters
                )
                content = response.choices[0].message.content.strip()
                
                try:
                    data = json.loads(content)
                    if isinstance(data, dict):
                        return [data]
                    elif isinstance(data, list):
                        return data
                    else:
                        raise ValueError("返回的数据格式不正确")
                except json.JSONDecodeError:
                    raise ValueError("返回的不是有效的JSON格式")
                    
            except Exception as e:
                print(f"生成数据时发生错误: {str(e)}")
                raise e
        
        return await _generate()
    
    def validate_config(self) -> bool:
        return bool(self.client and self.model_name)
