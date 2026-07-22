#!/usr/bin/env bash
# Fetch a hosted README card and write it to $2, but only if the response is
# genuinely an SVG. These services return HTTP 200 with an HTML error page when
# rate-limited, which would otherwise silently replace a good card with garbage.
set -euo pipefail

url="$1"
dest="$2"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

if ! curl -sfL --max-time 30 --retry 2 --retry-delay 5 "$url" -o "$tmp"; then
  echo "WARNING: fetch failed for $dest — keeping existing card" >&2
  exit 0
fi

if ! grep -qi '<svg' "$tmp"; then
  echo "WARNING: response for $dest was not an SVG — keeping existing card" >&2
  exit 0
fi

mkdir -p "$(dirname "$dest")"
mv "$tmp" "$dest"
trap - EXIT
echo "Updated $dest ($(wc -c < "$dest") bytes)"
