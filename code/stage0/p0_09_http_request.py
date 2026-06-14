"""
P0-09 HTTP 请求。

运行：
    python code/stage0/p0_09_http_request.py

任务：
    1. 使用 requests 请求一个公开 API。
    2. 打印 status_code、部分 headers、JSON。
    3. 设置 timeout，并处理请求失败。
"""


API_URL = "https://api.github.com"


def fetch_json(url):
    try:
        import requests
    except ImportError:
        return {"error": "请先安装 requests：pip install requests"}

    try:
        response = requests.get(url, timeout=10)
        headers = dict(list(response.headers.items())[:5])
        data = response.json()
        return {
            "status_code": response.status_code,
            "headers_sample": headers,
            "json": data,
        }
    except requests.exceptions.Timeout:
        return {"error": "请求超时"}
    except requests.exceptions.RequestException as exc:
        return {"error": f"请求失败：{exc}"}
    except ValueError:
        return {"error": "响应不是合法 JSON"}


def main():
    result = fetch_json(API_URL)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
