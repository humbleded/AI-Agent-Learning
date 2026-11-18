"""Check the published Vue app and its Nginx-to-FastAPI route."""

import argparse
import json
import sys
import time
from html.parser import HTMLParser
from http.client import HTTPException
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, build_opener


class EntryScripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        src = attrs.get("src") or ""
        if tag != "script" or attrs.get("type") != "module":
            return
        if src.startswith("/assets/") and urlsplit(src).path.endswith(".js"):
            self.paths.append(src)


def fetch(url, content_types):
    # Check the deployment directly, even on hosts with an HTTP proxy configured.
    opener = build_opener(ProxyHandler({}))
    deadline = time.monotonic() + 60
    while True:
        try:
            with opener.open(url, timeout=15) as response:
                content_type = response.headers.get_content_type()
                if response.status != 200 or content_type not in content_types:
                    raise ValueError(f"{url} returned HTTP {response.status}, {content_type}")
                body = response.read()
                if not body:
                    raise ValueError(f"{url} returned an empty body")
                return body
        except (OSError, HTTPException) as error:
            if isinstance(error, HTTPError) and error.code not in (502, 503, 504):
                raise ValueError(f"{url}: {error}") from error
            if time.monotonic() >= deadline:
                raise ValueError(f"{url} did not become ready: {error}") from error
            time.sleep(2)


def check(base_url):
    scripts = EntryScripts()
    scripts.feed(fetch(f"{base_url}/studio", {"text/html"}).decode())
    if not scripts.paths:
        raise ValueError("/studio has no built JavaScript module under /assets/")
    for path in scripts.paths:
        fetch(base_url + path, {"application/javascript", "text/javascript"})
        print(f"OK /studio -> {path}")

    health = json.loads(fetch(f"{base_url}/api/health", {"application/json"}))
    if not isinstance(health, dict) or not isinstance(health.get("modules"), list):
        raise ValueError("/api/health returned an unexpected response structure")
    modules = {
        row["id"]: row.get("status")
        for row in health["modules"]
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    expected = {"incidents": "available", "rag": "ready_to_run"}
    if health.get("status") != "ok" or any(modules.get(key) != value for key, value in expected.items()):
        raise ValueError(f"/api/health status={health.get('status')!r}, modules={modules}")
    print("OK /api/health: incidents=available, rag=ready_to_run")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", help="e.g. http://127.0.0.1:8081")
    args = parser.parse_args()
    try:
        check(args.base_url.rstrip("/"))
    except ValueError as error:
        sys.exit(f"Workbench check failed: {error}")
