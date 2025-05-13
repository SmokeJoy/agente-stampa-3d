#!/bin/bash
set -e # Esce immediatamente se un comando esce con stato non-zero.

echo "=== Starting simplified script in container ==="
cd /workspace

echo "=== Running poetry lock (no update) ==="
poetry lock --no-update

echo "=== Running poetry install (no root, no interaction) ==="
poetry install --no-root --no-interaction

echo "=== Generating Spectral lint log (run #2) ==="
spectral_output_file="/workspace/evidence/logs/spectral_lint_run2.log"
timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

# Esegue spectral e cattura l'output e l'exit code
# Prima scrive il timestamp, poi l'output di spectral
echo "$timestamp" > "$spectral_output_file"
spectral lint --ruleset /workspace/.config/.spectral.yaml --format text openapi_3_1_demo.json >> "$spectral_output_file"
SPECTRAL_EXIT_CODE=$?

echo "=== Content of $spectral_output_file: ==="
cat "$spectral_output_file"

echo "=== Spectral lint finished with exit code: $SPECTRAL_EXIT_CODE ==="
echo "=== Simplified script finished ==="
exit $SPECTRAL_EXIT_CODE 