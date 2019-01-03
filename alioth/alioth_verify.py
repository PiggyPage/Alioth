#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/27
# @File    : alioth_verify.py
# @Desc    : ""

import sys
from alioth.lib.core.option import get_options
from alioth.lib.controller.controller import start


def main():
    start(get_options(sys.argv))
