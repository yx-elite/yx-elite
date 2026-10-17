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

# GitHub only counts contributions one year at a time, so ask which years have
# any, then fetch every year in a single query (one alias per year) and add them up.
years="$(gh api graphql -F login="$login" -f query='
  query($login: String!) {
    user(login: $login) { contributionsCollection { contributionYears } }
  }' --jq '.data.user.contributionsCollection.contributionYears[]')"

per_year=""
for y in $years; do
  per_year+="y$y: contributionsCollection(from: \"$y-01-01T00:00:00Z\", to: \"$y-12-31T23:59:59Z\") {
        contributionCalendar { totalContributions }
      }
      "
done

# contributionsCollection with no dates is the past year.
gh api graphql -F login="$login" -f query="
  query(\$login: String!) {
    user(login: \$login) {
      followers { totalCount }
      repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
        totalCount
        nodes { stargazerCount }
      }
      contributionsCollection {
        contributionCalendar { totalContributions }
      }
      $per_year
    }
  }" --jq '.data.user | {
    stars: ([.repositories.nodes[].stargazerCount] | add // 0),
    contributions: .contributionsCollection.contributionCalendar.totalContributions,
    total_contributions: ([to_entries[] | select(.key | test("^y[0-9]{4}$")) | .value.contributionCalendar.totalContributions] | add // 0),
    followers: .followers.totalCount,
    repos: .repositories.totalCount
  }' | jq . > "$out"

echo "Updated $out"
cat "$out"
