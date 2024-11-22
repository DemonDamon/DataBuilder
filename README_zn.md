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

   # 加载环境变量
   load_dotenv()

   # 配置 OpenAI 客户端
   client = OpenAI(
       base_url=os.getenv("OPENAI_API_BASE"),
       api_key=os.getenv("OPENAI_API_KEY")
   )

   messages = []
   print("欢迎使用 GPT-3.5 聊天！(输入 'quit' 退出，'clear' 清除历史)")
```

参考代码块：
```python:examples/chat_completion.py
startLine: 78
endLine: 106
```

继续翻译：

```markdown:README_zn.md
2. 生成数据示例：

    a. 快速生成（generate_data.py）：
    ```python
    from src.core.builder import DataBuilder, TaskConfig, ModelConfig

    # 配置任务
    task_config = TaskConfig(
        description="生成中文情感分析数据集",
        examples=[
            {"text": "服务很好，食物美味", "label": "正面"},
            {"text": "太贵了而且等待时间长", "label": "负面"}
        ],
        schema={
            "format": "json",
            "fields": [
                {"name": "text", "type": "string"},
                {"name": "label", "type": "string", "choices": ["正面", "负面", "中性"]}
            ]
        }
    )

    # 配置模型
    model_config = ModelConfig(
        type="openai",
        model="gpt-3.5-turbo"
    )
    ```

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