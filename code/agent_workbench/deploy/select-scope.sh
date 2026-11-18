#!/usr/bin/env bash
# Select the images to check or release from the trees actually in use.
set -euo pipefail
: "${GITHUB_SHA:?}" "${GITHUB_OUTPUT:?}" "${EVENT_NAME:?}"
classifier=$(dirname -- "${BASH_SOURCE[0]}")/changed-services.py
# The repository point agreed when admitting the pre-Git cloud images.
# This is a tracking boundary, not the revision that built those images.
legacy_cutover=9765d20fb9fdd2aa8a54f24ba3e8beb1b746ff68

case ${REQUESTED_SCOPE:-auto} in
    web|api|both)
        printf 'scope=%s\n' "$REQUESTED_SCOPE" >> "$GITHUB_OUTPUT"
        exit 0 ;;
    auto) ;;
    *) echo "Unknown requested scope: $REQUESTED_SCOPE" >&2; exit 2 ;;
esac

valid_sha() { [[ $1 =~ ^[0-9a-f]{40}$ ]]; }
has_commit() { git cat-file -e "$1^{commit}" 2>/dev/null; }
require_commit() {
    if ! valid_sha "$1" || ! has_commit "$1"; then
        echo "Expected a commit from the full checkout: $1" >&2
        exit 1
    fi
}

tip=$GITHUB_SHA
require_commit "$tip"
case $EVENT_NAME in
    pull_request)
        require_commit "${PR_HEAD:?}"
        require_commit "${PR_BASE:?}"
        tip=$PR_HEAD
        base=$(git merge-base "$PR_BASE" "$tip") ;;
    push)
        if [[ ${EVENT_BEFORE:?} == 0000000000000000000000000000000000000000 ]]; then
            # A new branch has no previous push. Only its own changes count.
            base=$(git merge-base refs/remotes/origin/main "$tip" 2>/dev/null || git mktree </dev/null)
        elif ! valid_sha "$EVENT_BEFORE"; then
            echo "Invalid push baseline." >&2; exit 2
        elif has_commit "$EVENT_BEFORE"; then
            base=$EVENT_BEFORE
        else
            echo "Previous push commit is unavailable; both services need checking." >&2
            base=
        fi ;;
    workflow_dispatch)
        # A repository's first commit is compared to an empty tree.
        base=$(git rev-parse --verify "$tip^" 2>/dev/null || git mktree </dev/null) ;;
    *) echo "Unsupported event: $EVENT_NAME" >&2; exit 2 ;;
esac

event_scope=both
if [[ -n $base ]]; then
    event_scope=$(python3 "$classifier" "$base" "$tip")
fi
selected=()
for service in web api; do
    if [[ $service == web ]]; then live=${LIVE_WEB_BASE:-}; else live=${LIVE_API_BASE:-}; fi
    scope=$event_scope
    if [[ -n $live ]]; then
        if [[ $live == legacy ]]; then
            live=$legacy_cutover
            echo "$service uses a legacy image; tracking repository changes since $live." >&2
        fi
        if ! valid_sha "$live"; then echo "Invalid live $service baseline." >&2; exit 2; fi
        if has_commit "$live"; then
            scope=$(python3 "$classifier" "$live" "$tip")
        else
            echo "Active $service baseline is unavailable; selecting $service." >&2
            scope=$service
        fi
    fi
    if [[ $scope == both || $scope == "$service" ]]; then selected+=("$service"); fi
done

case ${#selected[@]} in
    0) scope=none ;;
    1) scope=${selected[0]} ;;
    2) scope=both ;;
esac
echo "Selected workbench scope: $scope"
printf 'scope=%s\n' "$scope" >> "$GITHUB_OUTPUT"
