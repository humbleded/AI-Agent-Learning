#!/usr/bin/env bash
# Run from code/agent_workbench on the GitHub runner with production credentials.
set +x
set -euo pipefail
source deploy/ssh-session.sh

digest=${ARTIFACT_DIGEST#sha256:}
if [[ ! $ARTIFACT_ID =~ ^[1-9][0-9]*$ || ! $digest =~ ^[0-9a-f]{64}$ || ! $GITHUB_SHA =~ ^[0-9a-f]{40}$ ]]; then
    echo "Invalid artifact ID, SHA-256 digest, or commit SHA." >&2
    exit 2
fi
case $RELEASE_SCOPE in
    web|api|both) ;;
    *) echo "Expected release scope web, api, or both." >&2; exit 2 ;;
esac
token=${GH_TOKEN:?Set a GitHub token with Actions read access}
unset GH_TOKEN
endpoint="$GITHUB_API_URL/repos/$GITHUB_REPOSITORY/actions/artifacts/$ARTIFACT_ID"

github_api() {
    curl --disable --silent --show-error --fail --globoff --proto '=https' \
        --connect-timeout 10 --max-time 45 --header @- \
        --header 'Accept: application/vnd.github+json' --header 'X-GitHub-Api-Version: 2022-11-28' \
        "$@" < <(printf 'Authorization: Bearer %s\n' "$token")
}

check_main() {
    git fetch --quiet --depth=1 origin refs/heads/main
    if [[ $(git rev-parse FETCH_HEAD) == "$GITHUB_SHA" ]]; then return; fi
    if ! git diff --quiet "$GITHUB_SHA" FETCH_HEAD -- '../../.github/workflows/workbench-web.yml' \
         'deploy/*.sh' deploy/check-workbench.py deploy/changed-services.py; then
        echo "Deployment instructions changed on main. Start a release from the new commit." >&2
        return 1
    fi
    local changed
    changed=$(python3 deploy/changed-services.py "$GITHUB_SHA" FETCH_HEAD)
    if [[ $changed != none && ( $changed == both || $RELEASE_SCOPE == both || $changed == "$RELEASE_SCOPE" ) ]]; then
        echo "New $changed changes on main overlap this $RELEASE_SCOPE release. Start a release from the new commit." >&2
        return 1
    fi
}

check_main
size=$(github_api --retry 2 "$endpoint" | python3 -c '
import json, sys
artifact = json.load(sys.stdin)
if artifact.get("expired") is not False or artifact.get("digest") != "sha256:" + sys.argv[1]:
    sys.exit("GitHub artifact expired or its digest differs from the build output.")
size = artifact.get("size_in_bytes")
if type(size) is not int or not 0 < size < 10**12:
    sys.exit("Invalid artifact size from GitHub.")
print(size)
' "$digest")
echo "Preparing $RELEASE_SCOPE release $GITHUB_SHA from artifact $ARTIFACT_ID ($size bytes)."

download() {
    local redirect
    redirect=$(github_api --header 'Cache-Control: no-cache' --output /dev/null \
        --write-out '%{http_code} %{redirect_url}' "$endpoint/zip") || return 75
    if [[ $redirect != '302 https://'* || $redirect == *[[:cntrl:]]* ]]; then
        echo "GitHub did not return an HTTPS artifact download redirect." >&2
        return 1
    fi
    printf '%s\n' "${redirect#302 }" |
        "${cloud[@]}" "bash '$stage/receive-images.sh' '$digest' '$size'"
}

# The outer shell retains ssh-session.sh's cleanup for the local key files.
(
    stage=$("${cloud[@]}" 'mktemp -d /tmp/ai-workbench-release.XXXXXXXX')
    if [[ ! $stage =~ ^/tmp/ai-workbench-release\.[A-Za-z0-9]{8}$ ]]; then
        echo "Unexpected remote staging directory." >&2
        exit 1
    fi
    cleanup_stage() {
        "${cloud[@]}" "rm -f -- '$stage/receive-images.sh' '$stage/apply-release.sh' '$stage/check-workbench.py' && rmdir -- '$stage'" </dev/null ||
            echo "Could not clean up the remote deployment scripts in $stage." >&2
    }
    trap cleanup_stage EXIT
    trap 'exit 129' HUP
    trap 'exit 130' INT
    trap 'exit 143' TERM
    tar -C deploy -cf - receive-images.sh apply-release.sh check-workbench.py |
        "${cloud[@]}" "tar -C '$stage' -xf -"

    for attempt in 1 2 3; do
        echo "Starting cloud download attempt $attempt of 3."
        status=0
        download || status=$?
        if (( status == 0 )); then break; fi
        if (( status != 75 || attempt == 3 )); then exit "$status"; fi
        echo "Requesting a fresh download link to resume the cached archive."
    done
    check_main
    "${cloud[@]}" "WORKBENCH_RELEASE_DIR=\"\$HOME/$RELEASE_DIRNAME\" bash '$stage/apply-release.sh' '$GITHUB_SHA' '$RELEASE_SCOPE'"
)
