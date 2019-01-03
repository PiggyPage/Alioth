#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : data.py
# @Desc    : ""

from time import strftime, localtime
from alioth import __version__ as version


class OPTIONS_DATA:
    USAGE = "\033[01;34m[*] Usage: python alioth.py -t <target> -p <poc_path or all>\033[0m\n\n"
    USAGE += " -t        TARGET         Target URL (e.g. 'http://www.targetsite.com/')\n"
    USAGE += " -f        TARGET_FILE    TARGET FILE (e.g. '/tmp/target.txt')\n"
    USAGE += " -p        POC_FILE       POC_FILE  (e.g. 'pocs/_0001_cms_sql_inj.py') or all\n"
    USAGE += " --thread  THREADS        Max number of concurrent HTTP(s) requests (default 5)"


class VIEW_DATA:
    BANNER = """\033[01;33m
    _     _  _         _    _     
   / \   | |(_)  ___  | |_ | |__  
  / _ \  | || | / _ \ | __|| '_ \ 
 / ___ \ | || || (_) || |_ | | | |
/_/   \_\|_||_| \___/  \__||_| |_|\n\033[0m"""

    VERSION = "\033[01;33m[Version: {}]\033[0m".format(version)
    POWERED = "\033[01;33m[Powered by jeffzhang <jeffzh3ng@gmail.com>]\033[0m\n"
    START_DATE = "[*] starting at " + strftime("%H:%M:%S", localtime()) + "\n"


class SCAN_RESULT:
    SUCCESS_COUNT = 0
    RESULT = []


class LOG_CONFIG:
    LOG_QUIET = False
