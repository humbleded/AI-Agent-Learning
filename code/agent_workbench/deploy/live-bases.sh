#!/usr/bin/env bash
# Report the deployed Git commit for each running service to the next Actions step.
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/ssh-session.sh"
: "${GITHUB_OUTPUT:?Missing GitHub Actions output file}"

snapshot=$("${cloud[@]}" "bash -s -- '$RELEASE_DIRNAME'" <<'REMOTE'
set -euo pipefail
cd -- "$HOME/$1"
for service in web api; do
    id=$(sudo -n docker compose ps --status running --quiet "$service")
    if [[ -z $id || $id == *$'\n'* ]]; then
        echo "Expected exactly one running container for $service." >&2
        exit 1
    fi
    sudo -n docker inspect --type container --format '{{.State.Running}} {{.Config.Image}}' "$id"
done
REMOTE
)

mapfile -t rows <<< "$snapshot"
if (( ${#rows[@]} != 2 )); then
    echo "Unexpected output from the deployment host." >&2
    exit 1
fi
services=(web api)
outputs=()
for i in "${!services[@]}"; do
    service=${services[i]}
    row=${rows[i]}
    if [[ $row =~ ^true\ ai-workbench-$service:git-([0-9a-f]{40})$ ]]; then
        base=${BASH_REMATCH[1]}
    elif [[ $row =~ ^true\ ai-workbench-$service:[0-9a-f]{12}$ ]]; then
        base=legacy
    else
        echo "Unrecognized image reference or stopped container for $service." >&2
        exit 1
    fi
    outputs+=("${service}_base=$base")
done
printf '%s\n' "${outputs[@]}" >> "$GITHUB_OUTPUT"
