#!/usr/bin/env bash
# Run on the deployment host after the selected git-<sha> images are loaded.
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 || ! $1 =~ ^[0-9a-f]{40}$ ]]; then
    echo "Usage: bash apply-release.sh <full Git commit SHA> [web|api|both]" >&2
    exit 2
fi
sha=$1
case ${2-both} in
    web|api) services=("$2") ;;
    both) services=(web api) ;;
    *) echo "Deployment scope must be web, api, or both." >&2; exit 2 ;;
esac
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
checker="$script_dir/check-workbench.py"
test -r "$checker" || { echo "Missing deployment checker: $checker" >&2; exit 1; }
if [[ ${WORKBENCH_RELEASE_DIR:-} != /* || ! -d $WORKBENCH_RELEASE_DIR ]]; then
    echo "Set WORKBENCH_RELEASE_DIR to the existing absolute deployment directory." >&2
    exit 2
fi
cd -- "$WORKBENCH_RELEASE_DIR"
exec 9>.deploy.lock
flock -w 180 9 || { echo "Another deployment still holds the lock." >&2; exit 1; }

docker=(sudo -n docker)
for service in "${services[@]}"; do
    "${docker[@]}" image inspect "ai-workbench-$service:git-$sha" >/dev/null
done
port=$("${docker[@]}" compose config --format json | python3 -c '
import json, sys
ports = json.load(sys.stdin)["services"]["web"]["ports"]
print(next(p["published"] for p in ports if p.get("host_ip") == "127.0.0.1" and p["target"] == 80))
')
base_url="http://127.0.0.1:$port"
other=
container_state() {
    local id
    id=$("${docker[@]}" compose ps -q "$1") || return 1
    "${docker[@]}" inspect --format '{{.Id}} {{.State.StartedAt}}' "$id"
}
if (( ${#services[@]} == 1 )); then
    if [[ ${services[0]} == web ]]; then other=api; else other=web; fi
    before=$(container_state "$other")
    echo "Unselected $other before (ID StartedAt): $before"
fi

check_unselected() {
    [[ -n $other ]] || return 0
    local after
    after=$(container_state "$other") || return 1
    echo "Unselected $other after  (ID StartedAt): $after"
    if [[ $before != "$after" ]]; then
        echo "Unselected service $other changed during deployment." >&2
        return 1
    fi
}

stage=$(mktemp -d .deploy.XXXXXXXX)
rollback=0

up() {
    "${docker[@]}" compose up -d --pull never --no-build --no-deps "${services[@]}"
}

check() {
    python3 "$checker" "$base_url"
}

finish() {
    local status=$?
    trap - EXIT
    trap '' HUP INT TERM
    if (( status != 0 && rollback )); then
        echo "Deployment failed. Restoring previous images for ${services[*]}." >&2
        if mv -f "$stage/restore.yaml" compose.yaml && up && check; then
            echo "Previous images restored and verified for ${services[*]}." >&2
        else
            echo "Rollback verification failed. Check docker compose ps and logs." >&2
        fi
    fi
    if (( status != 0 )); then check_unselected || true; fi
    rm -r -- "$stage"
    exit "$status"
}
trap finish EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

# Both files start from the live configuration. Even when an earlier backup
# includes changes to other services, a retry can only roll back this scope.
cp -p compose.yaml "$stage/next.yaml"
cp -p compose.yaml "$stage/restore.yaml"
python3 - "$sha" "$stage" "${services[@]}" <<'PY'
import re
import sys
from pathlib import Path

def image_line(yaml, service):
    prefix = f"ai-workbench-{service}:".encode()
    pattern = rb"(?m)^[ \t]*image:[ \t]*['\"]?" + prefix + rb"(?P<tag>[\w.-]+)(?=['\"\s#]|$)"
    matches = list(re.finditer(pattern, yaml))
    if len(matches) != 1:
        sys.exit(f"Expected one {prefix.decode()} image in the release configuration")
    return matches[0]


def with_tags(yaml, tags):
    for service, tag in tags.items():
        start, end = image_line(yaml, service).span("tag")
        yaml = yaml[:start] + tag + yaml[end:]
    return yaml


stage = Path(sys.argv[2])
services = sys.argv[3:]
current = Path("compose.yaml").read_bytes()
candidate = with_tags(current, dict.fromkeys(services, b"git-" + sys.argv[1].encode()))
(stage / "next.yaml").write_bytes(candidate)
previous = Path("compose.previous.yaml")
if candidate == current and previous.is_file():
    backup = previous.read_bytes()
    tags = {service: image_line(backup, service).group("tag") for service in services}
    (stage / "restore.yaml").write_bytes(with_tags(current, tags))
PY

if ! cmp -s compose.yaml "$stage/next.yaml"; then
    cp -p compose.yaml "$stage/previous.yaml"
    mv -f "$stage/previous.yaml" compose.previous.yaml
    rollback=1
    mv -f "$stage/next.yaml" compose.yaml
elif ! cmp -s compose.yaml "$stage/restore.yaml"; then
    rollback=1
fi
up
for service in "${services[@]}"; do
    container=$("${docker[@]}" compose ps -q "$service")
    running=$("${docker[@]}" inspect --format '{{.Config.Image}}' "$container")
    if [[ $running != "ai-workbench-$service:git-$sha" ]]; then
        echo "Unexpected running image for $service: $running" >&2
        exit 1
    fi
done
check
check_unselected
rollback=0
echo "Applied git-$sha to ${services[*]}."
