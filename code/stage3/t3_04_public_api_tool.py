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
    """调用公开 API，只返回必要字段（别把巨大 JSON 全塞给模型）。

    步骤：
      1. import requests（没装就返回错误）。
      2. requests.get(url, timeout=...)，一定要设 timeout。
      3. 只挑必要字段返回，如 ok / status_code / server / rate_limit。
      4. 分别捕获 Timeout 和其他 RequestException，返回 {"ok": False, "error": ...}。
    """
    try:
        import requests
    except ImportError:
        return {"ok": False, "error": "请先安装 requests：pip install requests"}

    try:
        response = requests.get(url, timeout=5)
    except requests.Timeout:
        return {"ok": False, "error": "请求超时"}
    except requests.RequestException as exc:
        return {"ok": False, "error": f"请求失败：{exc}"}

    return {
        "ok": response.ok,
        "status_code": response.status_code,
        "server": response.headers.get("Server"),
        "rate_limit_limit": response.headers.get("X-RateLimit-Limit"),
        "rate_limit_remaining": response.headers.get("X-RateLimit-Remaining"),
    }


if __name__ == "__main__":
    print(public_api_tool())
