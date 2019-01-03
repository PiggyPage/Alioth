#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : option.py
# @Desc    : ""


import sys
import os
import re
import getopt
from alioth.lib.utils.log import logger
from alioth.lib.core.data import OPTIONS_DATA
from alioth.lib.core.settings import DEFAULT_SCAN_THREATS, DEFAULT_SCAN_THREAT_MAX, RE_POC_CHECK
from alioth import __version__ as version


def get_options(argv):
    """
    从命令行获取参数
    :param argv:
    :return: 返回 target poc
    """
    target = ''
    poc = ''
    target_file = ''
    thread = ''
    try:
        # 从命令行获取参数
        opts, args = getopt.getopt(argv[1:], "hvt:f:p:", ["target=", "poc=", "thread="])
    except getopt.GetoptError:
        logger.data(OPTIONS_DATA.USAGE)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logger.data(OPTIONS_DATA.USAGE)
            sys.exit()
        if opt == '-v':
            logger.data("alioth " + str(version))
            sys.exit()
        elif opt == "--thread":
            thread = int(arg)
        elif opt == '-t' or opt == "--target":
            target = arg
        elif opt == "-f":
            target_file = arg
        elif opt in ("-p", "--plugin"):
            # PoC 有两种指定的文件 或者 PoC 名称
            # 如果是 PoC 名称那么 PoC 脚本必须放在项目 pocs 目录下
            poc = arg
            if poc.endswith(".py"):
                # 如果是指定路径的文件直接返回
                poc = poc
            # 如果是 all 则扫描目录下所有插件
            elif poc == 'all':
                poc = os.path.abspath(os.path.dirname(__file__) + "/../../../pocs/")
            else:
                # 如果是 PoC 名 则拼接出 PoC 路径（
                poc = os.path.abspath(os.path.dirname(__file__) + "/../../../pocs/" + poc + ".py")
    return _opt_parse(target, poc, target_file, thread)


def _opt_parse(target, poc, target_file, thread):
    """
    对接收对参数进行处理
    :param target: 单个目标
    :param poc: 单个 PoC 或者 PoC 目录
    :param target_file: 文件
    :param thread: 线程数量
    :return: 只返回 target_list(list) poc_list(list) thread
    """
    target_list = []
    poc_list = []
    if target:
        target_list.append(target)
    elif target_file:
        with open(target_file) as target_read:
            for t in target_read:
                target_list.append(t)
    else:
        logger.data(OPTIONS_DATA.USAGE)
        sys.exit()
    if poc.endswith('.py'):
        poc_list.append(poc)
    elif os.path.isdir(poc):
        files = os.listdir(poc)
        for file_name in files:
            file = poc + '/' + file_name
            if file.endswith(".py"):
                if re.search(RE_POC_CHECK, open(file).read()):
                    poc_list.append(file)
    else:
        logger.data(OPTIONS_DATA.USAGE)
        sys.exit()
    if not thread:
        thread = DEFAULT_SCAN_THREATS
    if thread > DEFAULT_SCAN_THREAT_MAX:
        thread = DEFAULT_SCAN_THREAT_MAX
    return target_list, poc_list, thread

