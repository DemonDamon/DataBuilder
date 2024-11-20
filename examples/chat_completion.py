import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 配置OpenAI客户端
client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def chat_completion(messages: list):
    """获取对话回复"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        
        for chunk in response:
            # 首先检查 choices 列表是否为空
            if not chunk.choices:
                continue
                
            # 检查是否有 delta 属性
            if not hasattr(chunk.choices[0], 'delta'):
                continue
                
            # 检查是否是结束标记
            if not hasattr(chunk.choices[0].delta, 'content'):
                continue
                
            # 检查内容是否为空
            if chunk.choices[0].delta.content is None:
                continue
                
            yield chunk.choices[0].delta.content
                
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        return

def interactive_chat():
    """交互式对话"""
    messages = []
    print("欢迎使用GPT-3.5聊天！(输入 'quit' 退出, 输入 'clear' 清空对话历史)")
    
    while True:
        user_input = input("\n你: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'clear':
            messages = []
            print("对话历史已清空")
            continue
            
        messages.append({"role": "user", "content": user_input})
        print("\nGPT: ", end="", flush=True)
        
        assistant_message = ""
        for chunk in chat_completion(messages):
            if chunk:  # 确保chunk不是None
                print(chunk, end="", flush=True)
                assistant_message += chunk
        print()  # 添加换行
        
        if assistant_message:  # 只有在成功获得回复时才添加到历史
            messages.append({"role": "assistant", "content": assistant_message})

if __name__ == "__main__":
    interactive_chat()