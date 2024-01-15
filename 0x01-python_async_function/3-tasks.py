#!/usr/bin/env python3
"""task_wait_random function"""
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Regular function that returns an asyncio.Task for wait_random"""
    return asyncio.create_task(wait_random(max_delay))
