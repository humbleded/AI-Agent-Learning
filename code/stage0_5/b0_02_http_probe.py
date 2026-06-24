"""
B0-02 网络基础与 HTTP：URL 探测器。

运行：
    python code/stage0_5/b0_02_http_probe.py https://example.com

任务：
    1. 解析 URL 的主机名。
    2. 输出解析到的 IP。
    3. 发起 GET 请求，打印状态码、部分 headers、响应体前 500 字符。
    4. 设置 timeout，并区分 DNS 失败、连接失败、非 2xx。
"""

import socket
import sys
from urllib.parse import urlparse
import requests


def resolve_ip(hostname):
    """把主机名解析成 IP；解析失败返回 None。"""
    # TODO: socket.gethostbyname，捕获 socket.gaierror
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None
    #raise NotImplementedError("B0-02：实现 resolve_ip")


def fetch(url):
    """探测一个 URL：打印 hostname、IP、状态码、部分 headers、响应体前 500 字符。

    步骤：
      1. import requests（没装就提示安装）。
      2. urlparse 取出 hostname；非法 URL 给提示并返回。
      3. resolve_ip 解析 IP；解析失败（DNS）就提示并返回。
      4. requests.get(url, timeout=...)，分别捕获 Timeout / ConnectionError / 其他 RequestException。
      5. 打印 method、status_code、ok、部分 headers、响应体前 500 字符。
    """
    # TODO
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        print("非法 URL")
        return
    ip = resolve_ip(hostname)
    if not ip:
        print("DNS 解析失败")
        return
    print(f"Hostname: {hostname}")
    print(f"IP: {ip}")
    try:
        response = requests.get(url, timeout=5)
        print(f"Method: GET")
        print(f"Status Code: {response.status_code}")
        print(f"OK: {response.ok}")
        if(response.ok):
            print("成功")
        else:
            print("服务器返回错误（非 2xx）")
        print(f"Headers: {dict(list(response.headers.items())[:5])}")
        print(f"Body: {response.text[:500]}")
    except requests.Timeout:
        print("请求超时")
    except requests.ConnectionError:
        print("连接失败")
    except requests.RequestException as e:
        print(f"请求异常: {e}")
    #raise NotImplementedError("B0-02：实现 fetch")


def classify_status(code):
   code=int(code)//100
   if code==1:
       return "信息"
   elif code==2:
       return "成功"
   elif code==3:
       return "重定向"
   elif code==4:
       return "客户端错误"
   elif code==5:
       return "服务器错误"
   else:
       return "未知状态"



def main():
    """从命令行参数或 input 取 URL -> 调 fetch。"""
    # TODO
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("请输入 URL: ")
    fetch(url)
    #raise NotImplementedError("B0-02：实现 main")


if __name__ == "__main__":
    main()
