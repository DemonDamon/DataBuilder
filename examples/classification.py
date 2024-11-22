import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
from dotenv import load_dotenv
import pandas as pd

from src.core.agent import Agent
from src.environments.static import StaticEnvironment

from src.skills.classification import ClassificationSkill
from src.runtimes.openai import OpenAIRuntime


# 加载环境变量
load_dotenv()


# 准备训练数据
train_df = pd.DataFrame([
    ["这个产品质量很好", "正面"],
    ["包装破损,很失望", "负面"], 
    ["一般般,不算好也不算差", "中性"],
    ["物流速度快,服务态度好", "正面"],
    ["产品有质量问题,退货也不方便", "负面"]
], columns=["text", "sentiment"])

# 准备测试数据
test_df = pd.DataFrame([
    "这个价格还算合理",
    "做工非常精致,值得推荐",
    "送货太慢了,等了好久"
], columns=["text"])

async def main():
    agent = Agent(
        skills=ClassificationSkill(
            name='sentiment',
            instructions='对商品评论进行情感分类',
            labels={'sentiment': ["正面", "负面", "中性"]},
            input_template='评论文本: {text}',
            output_template='情感分类: {sentiment}'
        ),
        environment=StaticEnvironment(
            df=train_df,
            ground_truth_columns={'sentiment': 'sentiment'}
        ),
        runtimes={
            'default': OpenAIRuntime(
                model='gpt-4o-mini',
                base_url=os.getenv('OPENAI_API_BASE'),
                api_key=os.getenv('OPENAI_API_KEY'),
                temperature=0.7
            )
        }
    )

    # 训练模型
    await agent.learn(learning_iterations=3)
    
    # 获取优化后的提示词
    optimized_prompt = agent.get_optimized_prompt()
    print(f"\n优化后的提示词:\n```\n{optimized_prompt}\n```")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())