"""
T3-04 外部 API 工具。

运行：
    python code/stage3/t3_04_public_api_tool.py

任务：
    1. 调用公开 API 或 mock API。
    2. 设置 timeout。
    3. 只返回必要字段，不把巨大原始 JSON 全塞给模型。
"""


API_URL = "https://api.github.com"


def public_api_tool(url=API_URL):
    try:
        import requests
    except ImportError:
        return {"ok": False, "error": "请先安装 requests"}

    try:
        response = requests.get(url, timeout=8)
        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "server": response.headers.get("server"),
            "rate_limit": response.headers.get("x-ratelimit-limit"),
        }
    except requests.exceptions.Timeout:
        return {"ok": False, "error": "timeout"}
    except requests.exceptions.RequestException as exc:
        return {"ok": False, "error": str(exc)}


if __name__ == "__main__":
    print(public_api_tool())
