# Source on the hosted runner with the production environment credentials.
set +x
: "${DEPLOY_HOST:?Set WORKBENCH_HOST}" "${DEPLOY_USER:?Set WORKBENCH_USER}" "${DEPLOY_KEY:?Set WORKBENCH_SSH_KEY}" "${KNOWN_HOSTS:?Set WORKBENCH_KNOWN_HOSTS}"
if [[ ! $RELEASE_DIRNAME =~ ^[A-Za-z0-9_-][A-Za-z0-9._-]*$ ]]; then
    echo "Invalid release directory name" >&2
    exit 1
fi
umask 077
key_dir=$(mktemp -d)
trap 'rm -f "$key_dir/key" "$key_dir/known_hosts"; rmdir "$key_dir"' EXIT
printf '%s\n' "$DEPLOY_KEY" > "$key_dir/key"
printf '%s\n' "$KNOWN_HOSTS" > "$key_dir/known_hosts"
unset DEPLOY_KEY KNOWN_HOSTS
cloud=(ssh -T -i "$key_dir/key" -o IdentitiesOnly=yes -o BatchMode=yes
       -o StrictHostKeyChecking=yes -o "UserKnownHostsFile=$key_dir/known_hosts"
       -o ConnectTimeout=20 -o ServerAliveInterval=20 -- "$DEPLOY_USER@$DEPLOY_HOST")
