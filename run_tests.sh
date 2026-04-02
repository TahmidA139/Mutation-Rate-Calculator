#!/usr/bin/env bash
# run_tests.sh
# ─────────────────────────────────────────────────────────────────────────────
# Runs a series of test cases for the Mutation Rate Calculator.
# Usage:
#   bash run_tests.sh
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

FASTA="example.fasta"
REFERENCE="Reference_seq"
OUTPUT="test_results.csv"

echo "=============================================="
echo "  Mutation Rate Calculator — Test Suite"
echo "=============================================="
echo ""

# ── Test 1: List sequence IDs ─────────────────────────────────────────────────
echo "── Test 1: List IDs in the FASTA file ──"
python main.py --fasta "$FASTA" --list-ids
echo ""

# ── Test 2: Basic mutation rate (gaps ignored, default) ───────────────────────
echo "── Test 2: Mutation rates (gaps ignored) ──"
python main.py --fasta "$FASTA" --reference "$REFERENCE"
echo ""

# ── Test 3: Keep gap positions ────────────────────────────────────────────────
echo "── Test 3: Mutation rates (gaps counted) ──"
python main.py --fasta "$FASTA" --reference "$REFERENCE" --keep-gaps
echo ""

# ── Test 4: Save output to CSV ────────────────────────────────────────────────
echo "── Test 4: Save results to CSV ──"
python main.py --fasta "$FASTA" --reference "$REFERENCE" --output "$OUTPUT"
echo "CSV contents:"
cat "$OUTPUT"
echo ""

# ── Test 5: Error handling — bad FASTA path ───────────────────────────────────
echo "── Test 5: Error handling — missing file ──"
python main.py --fasta "nonexistent.fasta" --reference "$REFERENCE" || true
echo ""

# ── Test 6: Error handling — bad reference ID ─────────────────────────────────
echo "── Test 6: Error handling — unknown reference ID ──"
python main.py --fasta "$FASTA" --reference "DOES_NOT_EXIST" || true
echo ""

# ── Test 7: Error handling — missing --reference flag ─────────────────────────
echo "── Test 7: Error handling — missing --reference flag ──"
python main.py --fasta "$FASTA" || true
echo ""

echo "=============================================="
echo "  All tests completed."
echo "=============================================="
