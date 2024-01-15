#!/usr/bin/env python3
""" Asynchronous coroutine wait_n """
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Asynchronous routine that spawns wait_random n times
    """
    delays_list = []
    async def wait_random_and_append():
        delay = await wait_random(max_delay)
        delays_list.append(delay)

    await asyncio.gather(*(wait_random_and_append() for _ in range(n)))

    return sorted(delays_list)
