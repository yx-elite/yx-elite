#!/usr/bin/env bash

# Refresh assets/stats.json with live GitHub numbers for the README badges.
#
#   .github/scripts/stats.sh
#
# Needs the gh CLI signed in (locally) or GH_TOKEN set (in GitHub Actions).
# The README reads this file through shields.io dynamic JSON badges, so the
# keys below must match the `query=$.<key>` part of each badge URL.

set -euo pipefail

login="${GITHUB_LOGIN:-yx-elite}"
out="$(cd "$(dirname "$0")/../.." && pwd)/assets/stats.json"

# contributionsCollection defaults to the past year.
gh api graphql -F login="$login" -f query='
  query($login: String!) {
    user(login: $login) {
      followers { totalCount }
      repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
        totalCount
        nodes { stargazerCount }
      }
      contributionsCollection {
        contributionCalendar { totalContributions }
      }
    }
  }' --jq '.data.user | {
    stars: ([.repositories.nodes[].stargazerCount] | add // 0),
    contributions: .contributionsCollection.contributionCalendar.totalContributions,
    followers: .followers.totalCount,
    repos: .repositories.totalCount
  }' > "$out"

echo "Updated $out"
cat "$out"
