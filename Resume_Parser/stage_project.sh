#!/usr/bin/env bash
# POSIX-compatible staging helper for the project
# Run from the repository root (where manage.py lives):
#   ./stage_project.sh

set -euo pipefail

paths=(
  "Resume_Parser_App/"
  "Resume_Parser/"
  "manage.py"
  "sample_resume.txt"
)

echo "Staging selected paths:"
for p in "${paths[@]}"; do
  if [ -e "$p" ]; then
    echo "  git add -- '$p'"
    git add -- "$p"
  else
    echo "  Skipped (not found): $p"
  fi
done

echo
echo "Staged files (git status --short):"
git status --short

echo
echo "If you meant to run the PowerShell helper on Windows PowerShell, use:`n  powershell -File stage_project.ps1"
