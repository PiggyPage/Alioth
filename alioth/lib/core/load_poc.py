#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/25
# @File    : load_poc.py
# @Desc    : ""

import re
import os
import sys
from alioth.lib.utils.log import logger
from alioth.lib.core.settings import RE_POC_CHECK


class LoadPoC:
    """
    通过 PoC 文件名（完整） 载入 PoC 函数到 list
    """
    def __init__(self, poc_file):
        # 先判断文件是否存在
        if os.path.exists(poc_file):
            self.poc_file = poc_file
            try:
                # 根据文件名获取插件的 Path
                self.module_path = "/".join(self.poc_file.split('/')[0:-1])
                # 获取包名： 2018_12_12_redis_all_unauthorized
                self.pack_name = self.poc_file.split('/')[-1][0:-3]
                # PoC 文件内容
                self.poc_str = open(self.poc_file).read()
            except Exception as e:
                logger.error("load poc error: " + str(e))
        else:
            logger.error("load poc error: Not Found " + poc_file)
            sys.exit(0)

    def load_poc(self):
        """
        加载 PoC 文件
        :return: 返回 PoC 函数 (list)
        """
        class_list = []
        try:
            # 将 PoC 路径加入到环境变量
            sys.path.append(self.module_path)
            class_name = self._get_poc_class_name()
            # 加载模块
            __import__(self.pack_name)
            tmp_module = sys.modules[self.pack_name]
            class_list.append(getattr(tmp_module, class_name))
            logger.info("load poc " + self.pack_name + " success")
        except ImportError as e:
            logger.error("load poc " + self.pack_name + " error")
            logger.error("load poc error: " + str(e))
        except Exception as e:
            logger.error("load poc " + self.pack_name + " error")
            logger.error("load poc error: " + str(e))
        return class_list

    def _get_poc_class_name(self):
        """
        正则匹配出 PoC 的 class 名，如： TestPoC
        :return:
        """
        try:
            class_name = re.search(RE_POC_CHECK, self.poc_str).group(1)
        except Exception as e:
            class_name = ""
            logger.error("Illegal poc: " + str(e))
        return class_name
