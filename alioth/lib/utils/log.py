#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/25
# @File    : log.py
# @Desc    : ""

import logging
import time
from sys import stdout
from alioth.lib.core.data import LOG_CONFIG


def _format_message(level, message):
    if level == "INFO":
        message = "\033[1;36m[{time}] [*] {message}\033[0m".format(
            time=time.strftime("%H:%M:%S", time.localtime()), level=level, message=message
        )
    elif level == "SUCCESS":
        message = "\033[1;32m[{time}] [+] {message}\033[0m".format(
            time=time.strftime("%H:%M:%S", time.localtime()), level=level, message=message
        )
    elif level == "WARNING":
        message = "\033[1;33m[{time}] [-] {message}\033[0m".format(
            time=time.strftime("%H:%M:%S", time.localtime()), level=level, message=message
        )
    elif level == "ERROR":
        message = "\033[1;31m[{time}] [!] {message}\033[0m".format(
            time=time.strftime("%H:%M:%S", time.localtime()), level=level, message=message
        )
    else:
        message = "\033[1;30m[{time}] [#] {message}\033[0m".format(
            time=time.strftime("%H:%M:%S", time.localtime()), level=level, message=message
        )
    return message


class Logger:
    def __init__(self):
        self._logger = logging.getLogger("Alioth")
        self._logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(stdout)
        self._logger.addHandler(hdlr=stream_handler)

    def info(self, message):
        if not LOG_CONFIG.LOG_QUIET:
            self._logger.info(_format_message("INFO", message))

    def success(self, message):
        if not LOG_CONFIG.LOG_QUIET:
            self._logger.info(_format_message("SUCCESS", message))

    def warning(self, message):
        if not LOG_CONFIG.LOG_QUIET:
            self._logger.warning(_format_message("WARNING", message))

    def error(self, message):
        if not LOG_CONFIG.LOG_QUIET:
            self._logger.error(_format_message("ERROR", message))

    def debug(self, message):
        self._logger.info(_format_message("DEBUG", message))

    def data(self, message):
        if not LOG_CONFIG.LOG_QUIET:
            self._logger.info(message)


logger = Logger()
