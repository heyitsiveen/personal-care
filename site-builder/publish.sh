#!/bin/bash
# Puts the current build on the live site: commits the site files, pushes to GitHub, waits for the
# Pages deploy, then confirms the live page matches index.html. Run it after the build and checks pass:
#   bash site-builder/publish.sh "feat(top-picks): refresh top picks, 3 Oct 2026" ["optional body"]
# Only the site files below are committed; downloaded photos (images/*.jpg, images/photos.js) stay local.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
LIVE="https://heyitsiveen.github.io/personal-care/"
SITE_FILES=(index.html images site-builder get-photos.sh get-photos.command)
fail(){ echo "FAIL: $*"; exit 1; }

[ -n "${1:-}" ] || fail 'usage: bash site-builder/publish.sh "type(scope): summary" ["body"]'
[ -f index.html ] || fail "index.html is missing - run the build first"
[ "$(git branch --show-current 2>/dev/null)" = main ] || fail "not on the main branch"

git add -A -- "${SITE_FILES[@]}" || fail "git add failed"
if git diff --cached --quiet; then
  echo "note: no site changes to commit"
else
  if [ -n "${2:-}" ]; then git commit -q -m "$1" -m "$2"; else git commit -q -m "$1"; fi || fail "git commit failed"
  echo "committed $(git log -1 --format='%h %s')"
fi
other=$(git status --porcelain)
[ -z "$other" ] || printf 'note: left uncommitted (not site files):\n%s\n' "$other"

git push -q origin HEAD:main || fail "push rejected - GitHub has commits this folder lacks: git pull --rebase, rebuild, publish again"
sha=$(git rev-parse HEAD)

# Wait for this commit's deploy run (skipped without gh; the live check below still waits).
if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then
  id=""
  for _ in $(seq 1 30); do
    id=$(gh run list --workflow deploy.yml --commit "$sha" --limit 1 --json databaseId --jq '.[0].databaseId // empty' 2>/dev/null)
    [ -n "$id" ] && break
    sleep 3
  done
  [ -n "$id" ] || fail "no deploy run started for ${sha:0:7} - check the Actions tab on GitHub"
  gh run watch "$id" --exit-status --interval 5 >/dev/null 2>&1 || fail "deploy failed - see: gh run view $id --log-failed (retry: gh run rerun $id)"
fi

for _ in $(seq 1 30); do
  if curl -fsSL --max-time 20 "$LIVE?v=$sha" | cmp -s - index.html; then
    echo "OK: live site updated - $LIVE (commit ${sha:0:7})"
    exit 0
  fi
  sleep 6
done
fail "the live page still differs from index.html 3 minutes after the deploy - $LIVE"
