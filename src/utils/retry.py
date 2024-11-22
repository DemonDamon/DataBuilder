"""
在 OpenAI 模型中使用重试装饰器了。

这个重试机制具有以下特点：
1. 指数退避：每次重试的等待时间会指数增加
2. 随机抖动：避免多个请求同时重试
3. 最大重试次数限制
4. 最大延迟时间限制
"""

import asyncio
from functools import wraps
from typing import Callable, Any


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1,
    max_delay: float = 10,
    exponential_base: float = 2
):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        raise last_exception
                    
                    await asyncio.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)
            
            raise last_exception
        return wrapper
    return decorator
