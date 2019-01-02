#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : utils.py
# @Desc    : ""

import os
import random
import string
from alioth.lib.core.load_poc import LoadPoC
from alioth.lib.controller.coroutine import coroutine
from alioth.lib.core.data import SCAN_RESULT, LOG_CONFIG
from alioth.lib.utils.target_parse import target_parse


class AliothScanner:
    def __init__(self, target, poc):
        LOG_CONFIG.LOG_QUIET = True
        self.target = target
        self.poc_name = poc['name']
        self.pocstring = poc['pocstring']
        if 'mode' in poc.keys():
            self.mode = poc['mode']
        if 'debug' in poc.keys():
            LOG_CONFIG.LOG_QUIET = not (poc['debug'])
        self.thread = int(poc['thread'])
        self.poc_file = ''
        self.options = None

    def run(self):
        try:
            if type(self.target) == str:
                self.target = [self.target]
            self.target = target_parse(self.target)
            if self._save_poc():
                self.options = (self.target, [self.poc_file], self.thread)
                if self.options:
                    return self.scanner()
        except Exception as e:
            return "looks like something went wrong, you can enable debug mode {}".format(str(e))

    def scanner(self):
        task_list = []
        target_list, poc_list, thread = self.options
        class_list = []
        target_list = target_parse(target_list)
        for poc in poc_list:
            for poc_class in LoadPoC(poc).load_poc():
                class_list.append(poc_class)
        for scanner in class_list:
            for target in target_list:
                task_list.append((target, scanner))
        try:
            coroutine(task_list, thread)
            return SCAN_RESULT.RESULT
        except Exception as e:
            return "looks like something went wrong, you can enable debug mode {}".format(str(e))

    def _save_poc(self):
        try:
            with open(self._tmp_poc_filename(), 'w') as poc_input:
                poc_input.write(self.pocstring)
                return True
        except Exception as e:
            return "looks like something went wrong, you can enable debug mode {}".format(str(e))

    def _tmp_poc_filename(self):
        tmp_path = os.environ.get('TMPDIR')
        tmp_name = ''.join(random.sample(string.ascii_lowercase, 5))
        self.poc_file = "{}{}_{}.py".format(tmp_path, self.poc_name, tmp_name)
        return self.poc_file
