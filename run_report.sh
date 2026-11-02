#!/bin/bash
# Nightly revenue report for the 2025 orders.
# Run it from the repository folder: ./run_report.sh

# AI-generated line (Claude, Anthropic, 2 Nov 2026). Prompt: asked how to make run_report.sh stop when a step fails. Reviewed and tested by me.
set -euo pipefail

cd "$(dirname "$0")"
export OUT=${OUT:-$HOME/data/out}
mkdir -p "$OUT"
echo "Nightly report started: $(date '+%H:%M:%S')"
bash steps/extracts.sh
python3 steps/report.py
python3 steps/audit.py
python3 steps/segments.py
bash steps/stats.sh
echo "Nightly report finished: $(date '+%H:%M:%S')"
