#!/usr/bin/env bash

# Regenerate the badges in assets/badges/ for brands whose logos shields.io no
# longer ships (LinkedIn, AWS, VS Code, OpenAI).
#
#   .github/scripts/badges.sh
#
# Each logo lives in assets/icons/<icon>.svg. The script tints it, sends it to
# shields.io as the badge logo, and saves the finished badge as assets/badges/<name>.svg.
# To add a badge, add a line to BADGES below and run the script again.

set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"

# name | label | badge colour | icon | icon colour
BADGES=(
  "linkedin|LinkedIn|0A66C2|linkedin|white"
  "aws|AWS|FF9900|aws|white"
  "vscode|VS Code|007ACC|vscode|white"
  "chatgpt|ChatGPT|FFFFFF|openai|black"
)

mkdir -p "$root/assets/badges"

for badge in "${BADGES[@]}"; do
  IFS='|' read -r name label color icon fill <<< "$badge"

  logo="$(sed "s/<path /<path fill=\"$fill\" /" "$root/assets/icons/$icon.svg" | base64 | tr -d '\n')"
  logo="${logo//+/%2B}"          # a literal + would be read as a space
  label="${label// /%20}"

  curl -fsSL "https://img.shields.io/badge/$label-$color?style=for-the-badge&logo=data:image/svg+xml;base64,$logo" \
    -o "$root/assets/badges/$name.svg"
  echo "Updated assets/badges/$name.svg"
done
