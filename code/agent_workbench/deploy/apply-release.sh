#!/usr/bin/env bash
# Run on the deployment host after both git-<sha> images have been loaded.
set -euo pipefail

if [[ $# != 1 || ! $1 =~ ^[0-9a-f]{40}$ ]]; then
    echo "Usage: bash apply-release.sh <full Git commit SHA>" >&2
    exit 2
fi
sha=$1
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
"${docker[@]}" image inspect "ai-workbench-web:git-$sha" "ai-workbench-api:git-$sha" >/dev/null
port=$("${docker[@]}" compose config --format json | python3 -c '
import json, sys
ports = json.load(sys.stdin)["services"]["web"]["ports"]
print(next(p["published"] for p in ports if p.get("host_ip") == "127.0.0.1" and p["target"] == 80))
')
base_url="http://127.0.0.1:$port"
stage=$(mktemp -d .deploy.XXXXXXXX)
rollback=0

up() {
    "${docker[@]}" compose up -d --pull never --no-build web api
}

check() {
    python3 "$checker" "$base_url"
}

finish() {
    local status=$?
    trap - EXIT
    trap '' HUP INT TERM
    if (( status != 0 && rollback )); then
        echo "Deployment failed. Restoring compose.previous.yaml." >&2
        if cp -p compose.previous.yaml "$stage/restore.yaml" &&
           mv -f "$stage/restore.yaml" compose.yaml && up && check; then
            echo "Previous release restored and verified." >&2
        else
            echo "Rollback verification failed. Check docker compose ps and logs." >&2
        fi
    fi
    rm -r -- "$stage"
    exit "$status"
}
trap finish EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

# The offline package has two local image tags. Keep the rest of its YAML,
# including the site-specific port and volume configuration, byte-for-byte.
cp -p compose.yaml "$stage/next.yaml"
python3 - "$sha" "$stage/next.yaml" <<'PY'
import re
import sys
from pathlib import Path

target = Path(sys.argv[2])
text = target.read_bytes()
for service in (b"web", b"api"):
    prefix = b"ai-workbench-" + service + b":"
    pattern = rb"(?m)^([ \t]*image:[ \t]*['\"]?" + prefix + rb")[\w.-]+(?=['\"\s#]|$)"
    text, count = re.subn(pattern, rb"\g<1>git-" + sys.argv[1].encode(), text)
    if count != 1:
        sys.exit(f"Expected exactly one {prefix.decode()} image in compose.yaml")
target.write_bytes(text)
PY

if ! cmp -s compose.yaml "$stage/next.yaml"; then
    cp -p compose.yaml "$stage/previous.yaml"
    mv -f "$stage/previous.yaml" compose.previous.yaml
    rollback=1
    mv -f "$stage/next.yaml" compose.yaml
elif [[ -f compose.previous.yaml ]] && ! cmp -s compose.yaml compose.previous.yaml; then
    # A retry must preserve the last distinct release as its rollback target.
    rollback=1
fi
up
for service in web api; do
    container=$("${docker[@]}" compose ps -q "$service")
    running=$("${docker[@]}" inspect --format '{{.Config.Image}}' "$container")
    if [[ $running != "ai-workbench-$service:git-$sha" ]]; then
        echo "Unexpected running image for $service: $running" >&2
        exit 1
    fi
done
check
rollback=0
echo "Applied git-$sha."
