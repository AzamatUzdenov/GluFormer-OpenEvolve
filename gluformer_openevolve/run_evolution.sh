#!/usr/bin/env bash
# run_evolution.sh — OpenEvolve for GluFormer HbA1c prediction
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "First set your Anthropic key: export OPENAI_API_KEY='sk-ant-YOUR-ANTHROPIC-KEY'"
  exit 1
fi

echo ""
echo "=== GluFormer x OpenEvolve: HbA1c prediction from embeddings + GMI ==="
echo "  Program  : $SCRIPT_DIR/initial_program.py"
echo "  Evaluator: $SCRIPT_DIR/evaluator.py"
echo "  Config   : $SCRIPT_DIR/config.yaml"
echo "  Output   : $SCRIPT_DIR/openevolve_output/"
echo ""

python -m openevolve.cli \
  "$SCRIPT_DIR/initial_program.py" \
  "$SCRIPT_DIR/evaluator.py" \
  --config "$SCRIPT_DIR/config.yaml" \
  --iterations "${OPENEVOLVE_ITERATIONS:-20}" \
  --output "$SCRIPT_DIR/openevolve_output"

echo ""
echo "=== Evolution complete ==="
echo "  Best program : $SCRIPT_DIR/openevolve_output/best/best_program.py"
echo "  Run compare  : python $SCRIPT_DIR/compare.py"
