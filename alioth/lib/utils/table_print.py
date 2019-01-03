#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/27
# @File    : table_print.py
# @Desc    : ""

from alioth.lib.utils.prettytable import PrettyTable


def res_table_print(data_list):
    new_table = PrettyTable(['id', 'target', 'poc', 'app', 'version', 'mode', 'status'])
    new_table.align['id'] = 'l'
    new_table.align['target'] = 'l'
    new_table.align['poc'] = 'l'
    new_table.align['app'] = 'l'
    new_table.align['version'] = 'l'
    new_table.align['mode'] = 'l'
    new_table.align['status'] = 'l'
    vid = 0
    for data in data_list:
        vid += 1
        target = data['target']
        poc = data['name']
        app = data['app']
        version = data['version']
        mode = data['mode']
        status = data['status']
        new_table.add_row([vid, target, poc, app, version, mode, status])
    return new_table
