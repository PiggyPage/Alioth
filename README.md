# Alioth
开源远程漏洞检测框架

一款基于 `Python3` 的远程漏洞检测框架，写这个轮子的初衷是没找到合适的漏洞检测框架，之前一直使用知道创宇团队的 `Pocsuite`，但目前没有支持 `Python3`（在开发，但一直没有公开），
所以不打算等了自己造个简单点的轮子

## 快速使用

直接使用 `pip` 工具安装最新版本

```bash
pip install alioth
alioth --version
```

或者克隆本仓库代码

```bash
git clone http://git.
cd alioth && python alioth --version
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




## 调用接口

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
