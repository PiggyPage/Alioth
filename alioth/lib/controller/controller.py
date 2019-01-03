#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : controller.py
# @Desc    : ""

from time import strftime, localtime
from alioth.lib.core.data import VIEW_DATA, SCAN_RESULT
from alioth.lib.core.load_poc import LoadPoC
from alioth.lib.utils.target_parse import target_parse
from alioth.lib.utils.log import logger
from alioth.lib.controller.coroutine import coroutine
from alioth.lib.utils.table_print import res_table_print


def start(options):
    logger.data(VIEW_DATA.BANNER)
    logger.data(VIEW_DATA.VERSION)
    logger.data(VIEW_DATA.POWERED)
    logger.data(VIEW_DATA.START_DATE)

    task_list = []
    target_list, poc_list, thread = options
    class_list = []
    target_list = target_parse(target_list)
    for poc in poc_list:
        for poc_class in LoadPoC(poc).load_poc():
            class_list.append(poc_class)
    for scanner in class_list:
        for target in target_list:
            task_list.append((target, scanner))
    try:
        logger.data("")
        logger.info("Scanning")
        logger.info("Start {} threads".format(thread))
        logger.info("Tasks {}".format(len(task_list)))
        logger.data("")
        coroutine(task_list, thread)
    except Exception as e:
        logger.error("start coroutine error: " + str(e))
    logger.data("")
    logger.data(res_table_print(SCAN_RESULT.RESULT))
    logger.data("success: {} / {}".format(SCAN_RESULT.SUCCESS_COUNT, len(task_list)))
    logger.data("\n[*] shutting down at {}".format(strftime("%H:%M:%S", localtime())))
    result = SCAN_RESULT.RESULT
    SCAN_RESULT.RESULT = []
    return result

