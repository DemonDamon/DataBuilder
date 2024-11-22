import json
import yaml
from typing import Dict, Any, List
from pathlib import Path
import asyncio


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """加载YAML配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_json_data(data: List[Dict[str, Any]], output_path: str):
    """保存数据为JSON格式"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_jsonl_data(data: List[Dict[str, Any]], output_path: str):
    """保存数据为JSONL格式"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def create_prompt(task_description: str, examples: List[Dict[str, Any]]) -> str:
    """创建prompt模板"""
    prompt = f"任务描述：{task_description}\n\n示例数据：\n"
    for i, example in enumerate(examples, 1):
        prompt += f"示例{i}：{json.dumps(example, ensure_ascii=False)}\n"
    prompt += "\n请按照以上格式生成新的数据。"
    return prompt
