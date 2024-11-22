import asyncio
from pathlib import Path
from src.core.builder import DataBuilder
from src.utils.helpers import load_yaml_config


async def main():
    # 加载配置
    config = load_yaml_config('config/default_config.yaml')
    
    # 初始化数据生成器
    builder = DataBuilder(
        task_config=config['task'],
        model_config=config['model']
    )
    
    # 生成数据集
    dataset = await builder.generate_dataset(
        total_samples=config['generation']['total_samples'],
        batch_size=config['generation']['batch_size']
    )
    
    # 保存数据集
    output_path = Path('output/dataset.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    builder.save_dataset(dataset, str(output_path))

if __name__ == "__main__":
    asyncio.run(main())
