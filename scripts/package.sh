#!/usr/bin/env bash
# Build dist/easyenv-workspaces.zip and its .sha256, the two release assets
# the sshPilot plugin registry points at.
#
# The files sit at the root of the zip, the layout sshPilot's installer looks
# for first. Listed one by one rather than globbed, so a __pycache__ or a
# stray editor file never ships.
set -euo pipefail

cd "$(dirname "$0")/.."
src=easyenv_workspaces
out=dist
name=easyenv-workspaces.zip

files=(
  plugin.json
  __init__.py
  easyenv_api.py
  model.py
  connections.py
  page.py
  dialogs.py
  cli_config.py
  logos.py
  README.md
  LICENSE
)

version=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$src/plugin.json")
if [[ -n "${GITHUB_REF_NAME:-}" && "${GITHUB_REF_NAME}" == v* && "${GITHUB_REF_NAME#v}" != "$version" ]]; then
  echo "tag ${GITHUB_REF_NAME} does not match plugin.json version $version" >&2
  exit 1
fi

rm -rf "$out"
mkdir -p "$out"
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
for f in "${files[@]}"; do
  case "$f" in
    README.md|LICENSE) cp "$f" "$stage/" ;;
    *) cp "$src/$f" "$stage/" ;;
  esac
done
# Fixed timestamps, so the same source gives the same checksum.
find "$stage" -exec touch -d '2020-01-01T00:00:00Z' {} +
(cd "$stage" && zip -X -q "$OLDPWD/$out/$name" "${files[@]}")
(cd "$out" && sha256sum "$name" > "$name.sha256")
echo "$out/$name ($version)"
cat "$out/$name.sha256"
