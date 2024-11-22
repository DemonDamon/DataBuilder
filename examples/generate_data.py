from src.core.builder import DataBuilder, TaskConfig, ModelConfig

# 配置任务
task_config = TaskConfig(
    description="生成中文情感分析数据集，包含正面、负面和中性评论",
    examples=[
        {"text": "这家餐厅的服务态度很好，菜品也很美味", "label": "正面"},
        {"text": "价格太贵了，而且等待时间特别长", "label": "负面"}
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
    name="gpt-4",
    parameters={
        "temperature": 0.7,
        "max_tokens": 1000
    }
)

# 初始化数据生成器
builder = DataBuilder(task_config, model_config)

# 生成数据
data = builder.generate(batch_size=10)

# 保存数据
builder.save(data, "output/sentiment_dataset.json")
