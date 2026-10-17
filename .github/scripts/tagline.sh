#!/usr/bin/env bash

# Regenerate assets/tagline.svg from readme-typing-svg.
#
#   .github/scripts/tagline.sh "<permalink>"
#
# The permalink is written to the first line of the SVG as <!-- edit: ... -->.
# Open it, change the text, click "Copy Permalink", and pass it to this script.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 \"<permalink>\"" >&2
  exit 1
fi

permalink="$1"
out="$(cd "$(dirname "$0")/../.." && pwd)/assets/tagline.svg"

# The permalink points at the editor (/demo/?...); the image is served from /?...
image_url="${permalink/\/demo\/\?/?}"

# Keep the permalink as the first line of the SVG, for reference.
svg="$(curl -fsSL "$image_url")"
printf '<!-- edit: %s -->\n%s\n' "$permalink" "$svg" > "$out"
echo "Updated $out"
