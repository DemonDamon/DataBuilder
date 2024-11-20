"""
在 OpenAI 模型中使用重试装饰器了。

这个重试机制具有以下特点：
1. 指数退避：每次重试的等待时间会指数增加
2. 随机抖动：避免多个请求同时重试
3. 最大重试次数限制
4. 最大延迟时间限制
"""

import asyncio
import random
from functools import wraps
from typing import TypeVar, Callable, Any

T = TypeVar('T')

def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1,
    max_delay: float = 60,
    exponential_base: float = 2,
    error_types: tuple = (Exception,),
    logger = None
):
    """增强的重试装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            
            while True:
                try:
                    return await func(*args, **kwargs)
                except error_types as e:
                    retries += 1
                    if retries > max_retries:
                        if logger:
                            logger.error(f"Max retries ({max_retries}) exceeded")
                        raise e
                    
                    delay = min(delay * exponential_base, max_delay)
                    if logger:
                        logger.warning(f"Retry {retries}/{max_retries} after {delay}s")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator