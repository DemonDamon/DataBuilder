import os
from dotenv import load_dotenv
from openai import OpenAI
import asyncio

# 加载环境变量
load_dotenv()

# 配置OpenAI客户端
client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)


def test_api():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "你好，请回复一句话测试连接"}]
        )
        print("API 测试成功！")
        print("模型回复:", response.choices[0].message.content)
    except Exception as e:
        print("API 测试失败:", str(e))


if __name__ == "__main__":
    test_api()
