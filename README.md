# Alioth [![Python 3.5](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/) [![GPLv3](https://img.shields.io/badge/license-GPLv3-red.svg)](https://github.com/jeffzh3ng/Alioth/blob/master/LICENSE)

一款基于 `Python3` 的远程漏洞检测框架，写这个轮子的初衷是没找到合适的漏洞检测框架，之前一直使用知道创宇团队的 `Pocsuite`，但目前没有支持 `Python3`（在开发，但一直没有公开），
所以不打算等了自己造个简单点的轮子

## 快速使用

直接使用 `pip` 工具安装最新版本

```bash
pip install alioth
alioth -h
```

或者克隆本仓库代码

```bash
git clone https://github.com/jeffzh3ng/Alioth.git
cd Alioth/ && python3 alioth.py -h
```

或者下载压缩包解压使用


## 初步上手

功能比较简单，就是一个漏洞验证的框架，使用参数如下：

```bash
(/tmp) ➜ alioth -h
[*] Usage: python alioth.py -t <target> -p <poc_path or all>

 -t        TARGET         Target URL (e.g. 'http://www.targetsite.com/')
 -f        TARGET_FILE    TARGET FILE (e.g. '/tmp/target.txt')
 -p        POC_FILE       POC_FILE  (e.g. 'pocs/_0001_cms_sql_inj.py') or all
 --thread  THREADS        Max number of concurrent HTTP(s) requests (default 5)
```

- `-t` 参数指定单个目标（IP 、网段 `192.168.111.0/24` 或者 URL）
- `-f` 参数指定一个文件，扫描对象每行一个，支持 IP、网段以及 URL
- `-p` 参数指定扫描插件，可以是插件路径如：`/tmp/170815_redis_all_unauthorized.py`，或者指定目录如：`/tmp/`，将会选取目录下符合插件标准的插件进行扫描
- `--thread`  参数指定扫描并发数量，如：10，默认并发为 1，最大并发 50


[![alioth_usage](https://asciinema.org/a/X6eAlybTCn0f4x0Yo4LRtLS3N.svg)](https://asciinema.org/a/X6eAlybTCn0f4x0Yo4LRtLS3N)

## 插件编写

插件编写请遵循 `python3` 编码规范

插件继承自 `BasePoC` 类

`_verify` 函数内编写验证代码，`parse_result` 函数处理测试结果，`parse_result` 函数继承 `Output` 类，成功调用 `success` 失败调用 `fail`


```python
from alioth.lib.core.poc import BasePoC, Output


class RedisUnAuth(BasePoC):
    pid = '190102_test_test'
    name = 'test name'
    author = 'jeffzhang'
    app = 'test'
    version = '1.0.0'
    v_type = 'sql inject',
    desc = 'test desc',
    date = '2019.01.02',

    def _verify(self):
        result = {}
        try:
            if self.target:
                result['target'] = self.target
                result['result'] = "test result"
        except Exception as e:
            self.error = e
        return self.parse_result(result)

    def parse_result(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail(self.error)
        return output
```

## 外部应用集成 Alioth

Alioth 提供了对外接口用于集成

从 `alioth.api.utils` 引入 `AliothScanner` 类，传入 `target` 以及 `poc_info`，调用 `run` 方法返回测试结果，返回的结果为 `list`

`target` 可以为 `str` 或者 `list`，`target` 类型可以是 `ip`、域名或网络段。

`poc_info` 为字典类型，需包含 `name`、`pocstring` 以及 `thread` 扫描线程

其中 `name` 为扫描插件名称，`pocstring` 为 `poc` 内容，`thread` 为扫描并发，`int` 类型，最小为 `1` 最大为 `50`

示例代码：

```python
from alioth.api.utils import AliothScanner


def poc_scanner(target_list, poc_info):
    scanner = AliothScanner(target_list, poc_info)
    result = scanner.run()
    return result


if __name__ == '__main__':
    target = ['127.0.0.1', '192.168.111.0/24']
    poc = {
        'name': 'Redis unauthorized access',
        'pocstring': open('/tmp/170815_redis_all_unauthorized.py').read(),
        'mode': 'verify',
        'thread': 5
    }
    res = poc_scanner(target, poc)
    print(res)
```
