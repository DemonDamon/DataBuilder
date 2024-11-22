# DataBuilder 🚀
<div align="center">
<img src="assets/logo1.webp" width="520" alt="ragalaxy logo">
</div>

欢迎使用 **DataBuilder**！本项目利用大型语言模型的能力，为 AI 训练和评估创建高质量、定制化的数据集。无论您是在构建新的 AI 模型还是增强现有模型，DataBuilder 都能简化您的数据准备过程。

## 特性 🌟

- **自定义数据集生成**：使用先进的 AI 模型根据您的具体需求定制数据集
- **高质量与多样性**：确保数据集具有多样性，能代表真实场景
- **可扩展解决方案**：轻松扩展数据集生成以满足任何规模项目的需求
- **用户友好界面**：直观的设计使任何人都能轻松生成数据集，无需专业技术知识

## 开始使用 🏁

按照以下步骤开始使用 DataBuilder：

### 前置要求

- Python 3.10 或更高版本
- pip（Python 包管理器）

### 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/DemonDamon/DataBuilder.git
   cd DataBuilder
   ```

2. 安装所需包：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境：
   - 复制 `.env.example` 到 `.env`
   - 使用您的 OpenAI API 凭证更新 `.env` 文件：
   ```plaintext
   OPENAI_API_KEY=your-api-key-here
   OPENAI_API_BASE=https://api.openai.com/v1
   ```

4. 测试 API 连接：
   ```bash
   python examples/test_api.py
   ```
   如果成功，您将看到：
   ```
   API 测试成功！
   模型回复: 你好，请问有什么可以帮助您的吗？
   ```

### 使用方法

1. 交互式聊天示例：
   ```bash
   python examples/chat_completion.py
   ```
   这将启动与 GPT-3.5 的交互式聊天会话。您可以：
   - 输入消息并按回车键进行聊天
   - 输入 'clear' 清除聊天历史
   - 输入 'quit' 退出

   示例代码：
   ```python
    from dotenv import load_dotenv
    from openai import OpenAI
    import os

    # Load environment variables
    load_dotenv()

    # Configure OpenAI client
    client = OpenAI(
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY")
    )

    messages = []
    print("Welcome to GPT-3.5 Chat! (Type 'quit' to exit, 'clear' to clear history)")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break
        
        messages.append({"role": "user", "content": user_input})
        print("\nGPT: ", end="", flush=True)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        
        assistant_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                assistant_message += chunk.choices[0].delta.content
        
        if assistant_message:
            messages.append({"role": "assistant", "content": assistant_message})
        print()
    ```

    2. 生成数据示例：

        a. 快速生成（generate_data.py）：
        ```python
        from src.core.builder import DataBuilder, TaskConfig, ModelConfig

        # Configure task
        task_config = TaskConfig(
            description="Generate Chinese sentiment analysis dataset",
            examples=[
                {"text": "Great service and delicious food", "label": "positive"},
                {"text": "Too expensive and long waiting time", "label": "negative"}
            ],
            schema={
                "format": "json",
                "fields": [
                    {"name": "text", "type": "string"},
                    {"name": "label", "type": "string", "choices": ["positive", "negative", "neutral"]}
                ]
            }
        )

        # Configure model
        model_config = ModelConfig(
            type="openai",
            name="gpt-4",
            parameters={
                "temperature": 0.7,
                "max_tokens": 1000
            }
        )

        # Initialize and generate
        builder = DataBuilder(task_config, model_config)
        data = builder.generate(batch_size=10)
        ```

        b. 批量生成 (generate_dataset.py)：

        - 使用 YAML 配置
        - 支持异步处理
        - 处理大规模生成
        
        示例配置文件：config/default_config.yaml：
        ```yaml
        generation:
        batch_size: 10      # Number of samples per batch
        total_samples: 100  # Total number of samples to generate
        validation: true    # Enable data validation

        task:
        description: "Generate Chinese sentiment analysis dataset"
        examples: [...]
        schema: {...}

        model:
        type: "openai"
        name: "gpt-4"
        parameters:
            temperature: 0.7
            max_tokens: 1000
        ```
        
        运行生成器:
        ```bash
        python examples/generate_dataset.py
        ```

        主要区别：
        - `generate_data.py`：快速测试和小型数据集
        - `generate_dataset.py`：生产环境使用，具备：
            - 配置管理
            - 异步处理
            - 批量生成
            - 灵活的参数控制

        c. 情感识别分类样例 [classification.py](examples/classification.py):
        ```python
        from src.core.agent import Agent
        from src.environments.static import StaticEnvironment
        from src.skills.classification import ClassificationSkill
        from src.runtimes.openai import OpenAIRuntime
        import pandas as pd

        # 准备训练数据
        train_df = pd.DataFrame([
            ["这个产品质量很好", "正面"],
            ["包装破损,很失望", "负面"], 
            ["一般般,不算好也不算差", "中性"],
            ["物流速度快,服务态度好", "正面"],
            ["产品有质量问题,退货也不方便", "负面"]
        ], columns=["text", "sentiment"])

        # 创建代理
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
                    model='gpt-3.5-turbo',
                    api_key=os.getenv('OPENAI_API_KEY'),
                    temperature=0.7
                )
            }
        )

        # 训练模型
        await agent.learn(learning_iterations=3)
        ```

        特点:
        - **自动提示词优化**: 通过多轮训练自动优化提示词
        - **准确率反馈**: 每轮训练都会计算并显示准确率
        - **格式规范化**: 自动规范化模型输出格式
        - **渐进式学习**: 支持多轮迭代训练提升效果

        运行示例:
        ```bash
        python examples/classification.py
        ```

        输出示例:
        ~~~
        开始第 1 轮训练...
        训练准确率: {'sentiment_accuracy': 0.4}
        新提示词效果更好: 1.0 > 0.4
    
        开始第 2 轮训练...
        训练准确率: {'sentiment_accuracy': 1.0}
    
        开始第 3 轮训练...
        训练准确率: {'sentiment_accuracy': 1.0}
    
        优化后的提示词:
        ```
        对商品评论进行情感分类。
        输入模板: 评论文本: {text}
        输出模板: 情感分类: {sentiment}
        可用标签: {'sentiment': ['正面', '负面', '中性']}
        ```
        ~~~

### 常见问题

1. API 连接错误：
   - 验证您的 API 密钥是否正确
   - 检查是否需要使用代理（添加到 `.env`）：
     ```plaintext
     OPENAI_PROXY=http://127.0.0.1:7890
     ```
   - 确保您的 API 基础 URL 正确

## 参与贡献 🤝

我们欢迎社区贡献！如果您想贡献，请遵循以下步骤：

1. Fork 仓库
2. 创建新分支（`git checkout -b feature/您的功能`）
3. 提交更改（`git commit -m '添加某个功能'`）
4. 推送到分支（`git push origin feature/您的功能`）
5. 开启拉取请求

## 许可证 📄

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 联系方式 📬

如有任何问题或反馈，请通过 [bingzhenli@hotmail.com](bingzhenli@hotmail.com) 联系我们。

## 项目参考 🔍

本项目从 [Adala](https://github.com/HumanSignal/Adala) 框架汲取灵感，融合了几个关键的架构概念：

### 受 Adala 启发的核心组件

1. **基于代理的架构**
   - 自主数据生成代理
   - 迭代学习能力
   - 环境感知处理

2. **运行时系统**
   - 灵活的模型集成
   - 可配置的执行环境
   - 支持多个 LLM 提供商

3. **环境管理**
   - 真实数据集处理
   - 反馈收集机制
   - 性能指标追踪

4. **技能系统**
   - 特定任务能力
   - 可定制输出格式
   - 验证机制

### 主要改进

我们在采用 Adala 概念的同时进行了多项增强：

- **简化配置**：使用基于 YAML 的配置简化设置流程
- **异步处理**：为批处理操作添加强大的异步支持
- **增强验证**：改进数据质量检查和错误处理
- **指标收集**：添加全面的生成指标和监控

### 未来集成

受 Adala 启发的计划功能：
- 长期学习的记忆管理
- 高级反馈收集机制
- 多模态数据生成支持
- 增强运行时优化

有关 Adala 架构的更多详细信息，请参阅其文档。

## 🗺 未来里程碑

### 1. 增强代理架构
- [ ] 实现教师-学生模型架构（使用更强大的模型指导较弱模型）
- [ ] 支持多技能组合和协同
- [ ] 添加长期记忆管理机制
- [ ] 实现异步反馈收集机制

### 2. 环境系统增强
- [ ] 支持人工干预的反馈机制
- [ ] 添加实时环境交互能力
- [ ] 实现动态数据集管理
- [ ] 支持增量学习场景

### 3. 运行时优化
- [ ] 支持多 LLM 提供商（如 Claude、文心一言等）
- [ ] 实现模型性能自动评估
- [ ] 添加模型调用成本追踪
- [ ] 支持批量处理优化

### 4. 技能系统扩展
- [ ] 添加命名实体识别（NER）技能
- [ ] 实现多任务并行学习
- [ ] 支持跨语言技能迁移
- [ ] 添加文本生成技能模板

### 5. 工具链建设
- [ ] 提供命令行工具
- [ ] 实现 REST API 接口
- [ ] 支持 Jupyter Notebook 集成
- [ ] 添加 Web UI 界面

### 6. 监控与评估
- [ ] 实现详细的指标收集系统
- [ ] 添加性能可视化面板
- [ ] 支持实验对比分析
- [ ] 实现自动化测试框架

### 7. 多模态支持
- [ ] 添加图像处理能力
- [ ] 支持语音输入输出
- [ ] 实现跨模态技能
- [ ] 支持视频内容处理