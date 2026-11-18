"""Print web, api, both or none for the paths changed between two Git trees."""

import argparse
from fnmatch import fnmatchcase
import os
import subprocess


# Keep these patterns in sync with the Docker build contexts and CI tests.
# fnmatchcase's * includes nested paths, e.g. a Markdown file under public/.
IMAGE_INPUTS = {
    "code/agent_workbench/web/": ("web", (
        "src/*", "public/*", "test/*", "tests/*", "*.test.*", "*.spec.*",
        "Dockerfile*", ".dockerignore", "nginx.conf", "package*.json", ".npmrc",
        "index.html", "env.d.ts", "tsconfig*.json", "*.config.*",
    )),
    "code/agent_workbench/api/": ("api", (
        "*.py", "test/*", "tests/*", "Dockerfile*", ".dockerignore", "*requirements*.txt",
    )),
    "code/stage6/engineering_docs_rag/": ("api", (
        "ingest.py", "knowledge_agent.py", "*requirements.txt", "sample_docs/*",
        "tests/*", "test_*.py",
    )),
    "code/stage8/incident_change_review_agent/": ("api", (
        "incident_graph.py", "requirements.txt", "tests/*", "test_*.py",
    )),
}


def changed_services(paths):
    services = set()
    for path in paths:
        if path == "code/agent_workbench/compose.yaml":
            return "both"
        for prefix, (service, patterns) in IMAGE_INPUTS.items():
            if path.startswith(prefix):
                relative = path[len(prefix):]
                if any(fnmatchcase(relative, pattern) for pattern in patterns):
                    services.add(service)
                break
    return "both" if len(services) == 2 else next(iter(services), "none")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base")
    parser.add_argument("tip")
    args = parser.parse_args()
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
    diff = subprocess.check_output([
        "git", "diff", "--name-only", "--no-renames", "-z", "--end-of-options",
        args.base, args.tip, "--",
    ], cwd=root)
    print(changed_services(os.fsdecode(path) for path in diff.split(b"\0") if path))
