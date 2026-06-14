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


def resolve_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def fetch(url):
    try:
        import requests
    except ImportError:
        print("请先安装 requests：pip install requests")
        return

    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        print("URL 不合法，示例：https://example.com")
        return

    ip = resolve_ip(hostname)
    print("hostname:", hostname)
    print("ip:", ip or "DNS 解析失败")
    if ip is None:
        return

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        print("请求失败：timeout")
        return
    except requests.exceptions.ConnectionError as exc:
        print("请求失败：连接错误", exc)
        return
    except requests.exceptions.RequestException as exc:
        print("请求失败：", exc)
        return

    print("method: GET")
    print("status_code:", response.status_code)
    print("ok:", response.ok)
    print("headers_sample:", dict(list(response.headers.items())[:8]))
    print("body_sample:", response.text[:500])


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else input("URL：").strip()
    fetch(url)


if __name__ == "__main__":
    main()
