#!/usr/bin/env bash
# Read a short-lived HTTPS artifact URL on stdin. Exit 75 asks the runner
# to issue a fresh URL and resume the same archive.
set +x
set -euo pipefail
umask 077

if [[ $# != 2 || ! $1 =~ ^[0-9a-f]{64}$ || ! $2 =~ ^[1-9][0-9]{0,11}$ ]]; then
    echo "Usage: receive-images.sh <archive-sha256> <archive-bytes>" >&2
    exit 2
fi
digest=$1
size=$2
IFS= read -r url
if [[ $url != https://* || $url == *[[:cntrl:][:space:]]* || $url == *'"'* || $url == *'\'* ]]; then
    echo "Expected a single HTTPS download URL." >&2
    exit 2
fi

cache="$HOME/.cache/ai-workbench-delivery"
install -d -m 700 -- "$cache"
exec 9>"$cache/download.lock"
flock -w 30 9 || { echo "Another download is in progress." >&2; exit 1; }
part="$cache/$digest.zip.part"
touch -- "$part"
scratch=$(mktemp -d "$cache/import.XXXXXXXX")
curl_pid=
cleanup() {
    if [[ -n $curl_pid ]]; then
        kill "$curl_pid" 2>/dev/null || true
        wait "$curl_pid" 2>/dev/null || true
    fi
    rm -f -- "$scratch/http" "$scratch/images.tar.gz"
    rmdir -- "$scratch"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

received=$(stat -c %s "$part")
if (( received < size )); then
    echo "Downloading archive: $received / $size bytes cached."
    # Keep the signed URL out of process arguments, output and curl errors.
    curl --disable --config - --globoff --location --proto '=https' --proto-redir '=https' \
        --silent --fail --connect-timeout 20 --speed-time 90 --speed-limit 1024 \
        --max-time 1500 --continue-at - --output "$part" --write-out '%{http_code}' \
        < <(printf 'url = "%s"\n' "$url") > "$scratch/http" 2>/dev/null &
    curl_pid=$!
    next_report=$((SECONDS + 20))
    while kill -0 "$curl_pid" 2>/dev/null; do
        sleep 1
        if (( SECONDS >= next_report )); then
            echo "Downloading archive: $(stat -c %s "$part") / $size bytes cached."
            next_report=$((SECONDS + 20))
        fi
    done
    rc=0
    wait "$curl_pid" || rc=$?
    curl_pid=
    http=$(cat "$scratch/http")
    echo "Download result: HTTP ${http:-000}, curl $rc, $(stat -c %s "$part") / $size bytes cached."
    if (( received > 0 )) && { (( rc == 33 )) || [[ $http == 416 ]]; }; then
        rm -f -- "$part"
        echo "The endpoint rejected the byte range. The next attempt will start at zero." >&2
        exit 75
    fi
    case $rc in
        0) ;;
        6|7|16|18|22|28|35|52|55|56|92|95) exit 75 ;;
        *) exit 1 ;;
    esac
fi
unset url

if [[ $(stat -c %s "$part") != "$size" ]] || ! printf '%s  %s\n' "$digest" "$part" | sha256sum --check --status; then
    rm -f -- "$part"
    echo "Archive size or SHA-256 mismatch. Discarded the cached archive." >&2
    exit 65
fi
echo "Verified artifact SHA-256: $digest"

python3 - "$part" "$scratch/images.tar.gz" <<'PY'
import hashlib
import re
import sys
from zipfile import ZipFile

with ZipFile(sys.argv[1]) as archive:
    manifest = re.fullmatch(rb"([0-9a-f]{64})  images\.tar\.gz\n?", archive.read("SHA256SUMS"))
    if manifest is None:
        sys.exit("Invalid images.tar.gz checksum manifest.")
    digest = hashlib.sha256()
    with archive.open("images.tar.gz") as image, open(sys.argv[2], "wb") as output:
        while block := image.read(1024 * 1024):
            digest.update(block)
            output.write(block)
    if digest.hexdigest() != manifest[1].decode("ascii"):
        sys.exit("Image archive SHA-256 mismatch.")
PY
echo "Verified images.tar.gz; importing images from the cloud server's disk."
sudo -n docker image load --input "$scratch/images.tar.gz"
rm -f -- "$part"
