#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/27
# @File    : coroutine.py
# @Desc    : ""

import asyncio
from alioth.lib.utils.log import logger


def task_run(task):
    target, scanner = task
    logger.info("Testing: {} {}".format(target, scanner.name))
    try:
        scanner(target).run()
    except Exception as e:
        logger.error(e)
    logger.info("Done: {} {}".format(target, scanner.name))


async def async_run(task, semaphore):
    # 获取当前事件循环
    async_task = asyncio.get_event_loop()
    try:
        async with semaphore:
            # 新建一个线程来执行函数 防止阻塞
            await async_task.run_in_executor(None, task_run, task)
    except Exception as e:
        logger.error("async start error: " + str(e))


def coroutine(task_list, thread):
    try:
        # 将扫描任务协程 打包为一个 Task 排入日程准备执行 返回 Task 对象
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # 控制携程数量
        semaphore = asyncio.Semaphore(thread)
        tasks = [asyncio.ensure_future(async_run(task, semaphore)) for task in task_list]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception as e:
        logger.error(e)
