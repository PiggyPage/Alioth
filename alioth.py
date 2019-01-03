#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : alioth.py
# @Desc    : ""

import sys
from alioth.lib.core.option import get_options
from alioth.lib.controller.controller import start


if __name__ == '__main__':
    start(get_options(sys.argv))
