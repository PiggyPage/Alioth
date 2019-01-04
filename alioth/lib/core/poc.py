#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/25
# @File    : poc.py
# @Desc    : ""

from alioth.lib.core.data import SCAN_RESULT
from alioth.lib.utils.log import logger


class BasePoC:
    """
    PoC 插件父类 PoC 插件必须继承于 BasePoC
    """
    pid = None
    name = None
    author = None
    app = None
    version = None
    v_type = None
    desc = None
    date = None

    def __init__(self, target, mode='verify'):
        self.target = target
        self.mode = mode
        self.error = ''
        self.success_count = SCAN_RESULT.SUCCESS_COUNT

    def _verify(self, *args, **kwargs):
        pass

    def _attack(self,  *args, **kwargs):
        pass

    def run(self,  **kwargs):
        # 判断插件模式
        if self.mode == 'verify':
            # PoC 插件中进行重写 返回一个Output类实例
            return self._verify(**kwargs)
        elif self.mode == 'attack':
            # PoC 插件中进行重写 返回一个Output类实例
            return self._attack(**kwargs)


class Output(object):
    """
    结果输出
    """
    def __init__(self, poc_info=None):
        if poc_info:
            self.pid = poc_info.pid
            self.name = poc_info.name
            self.target = poc_info.target
            self.mode = poc_info.mode
            self.app = poc_info.app
            self.version = poc_info.version

    def success(self, result):
        # 成功调用这里
        tmp_result = {
            "target": self.target,
            "name": self.name,
            "app": self.app,
            "version": self.version,
            "mode": self.mode,
            "status": "success",
            "result": result
        }
        # 统计成功漏洞数量
        SCAN_RESULT.SUCCESS_COUNT += 1
        # 放到 data 中的 RESULT
        SCAN_RESULT.RESULT.append(tmp_result)
        msg = "{} {} [{}] is vulnerable".format(self.mode.capitalize(), self.target, self.name)
        logger.success(msg)

    def fail(self, error=""):
        # 失败调用这里
        tmp_result = {
            "target": self.target,
            "name": self.name,
            "app": self.app,
            "version": self.version,
            "mode": self.mode,
            "status": "failed",
            "result": {"extra": str(error)},
        }
        # 放到 data 中的 RESULT
        SCAN_RESULT.RESULT.append(tmp_result)
        msg = "{} {} [{}] failed: {}".format(self.mode.capitalize(), self.target, self.name, error)
        logger.warning(msg)
