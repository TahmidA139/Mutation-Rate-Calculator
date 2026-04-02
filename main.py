#!/usr/bin/env python3
"""
main.py
-------
Mutation Rate Calculator — entry point.

Usage examples
--------------
# List sequence IDs from a FASTA file
python main.py --fasta example.fasta --list-ids

# Run mutation-rate analysis using 'NC_045512.2' as the reference
python main.py --fasta example.fasta --reference "NC_045512.2"

# Save results to a CSV
python main.py --fasta example.fasta --reference "NC_045512.2" --output results.csv

# Include gap positions in the calculation
python main.py --fasta example.fasta --reference "NC_045512.2" --keep-gaps
"""

import argparse
import sys

import pandas as pd

from mut_calc.fasta_parser import parse_fasta, validate_alignment
from mut_calc.mutation_rate import build_mutation_table


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Return the configured ArgumentParser for this script."""
    parser = argparse.ArgumentParser(
        prog="mutation_rate_calculator",
        description=(
            "Calculate the per-sequence mutation rate of a FASTA alignment "
            "relative to a chosen reference sequence."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--fasta", "-f",
        required=True,
        metavar="FILE",
        help="Path to the aligned FASTA file.",
    )
    parser.add_argument(
        "--reference", "-r",
        metavar="SEQ_ID",
        help=(
            "Header of the reference sequence (as it appears after '>' in the "
            "FASTA file, without the '>'). Required unless --list-ids is used."
        ),
    )
    parser.add_argument(
        "--output", "-o",
        metavar="CSV_FILE",
        default=None,
        help="Optional path to save the results as a CSV file.",
    )
    parser.add_argument(
        "--keep-gaps",
        action="store_true",
        default=False,
        help=(
            "Include gap characters ('-', '.') when counting sites. "
            "By default, gap columns are ignored."
        ),
    )
    parser.add_argument(
        "--list-ids",
        action="store_true",
        default=False,
        help="Print the sequence IDs found in the FASTA file and exit.",
    )
    return parser


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class MutationRateAnalysis:
    """
    Orchestrates the full analysis pipeline:
      1. Parse the FASTA alignment.
      2. Optionally validate that all sequences have the same length.
      3. Compute mutation rates relative to a reference.
      4. Display and optionally save results.
    """

    def __init__(self, fasta_path: str, reference_id: str, ignore_gaps: bool = True):
        """
        Initialise the analysis.

        Parameters
        ----------
        fasta_path : str
            Path to the aligned FASTA file.
        reference_id : str
            Header of the sequence to use as the reference.
        ignore_gaps : bool
            Whether to exclude gap positions from the rate calculation.
        """
        self.fasta_path = fasta_path
        self.reference_id = reference_id
        self.ignore_gaps = ignore_gaps
        self.sequences: dict[str, str] = {}
        self.results: pd.DataFrame | None = None

    def load(self) -> None:
        """Parse the FASTA file and validate the alignment."""
        print(f"[INFO] Loading alignment from: {self.fasta_path}", file=sys.stdout)
        self.sequences = parse_fasta(self.fasta_path)
        print(f"[INFO] {len(self.sequences)} sequences found.", file=sys.stdout)
        validate_alignment(self.sequences)

    def run(self) -> None:
        """Compute mutation rates for all sequences against the reference."""
        print(f"[INFO] Reference sequence: {self.reference_id}", file=sys.stdout)
        self.results = build_mutation_table(
            self.sequences,
            reference_id=self.reference_id,
            ignore_gaps=self.ignore_gaps,
        )

    def display(self) -> None:
        """Print the results table to stdout."""
        if self.results is None or self.results.empty:
            print("[WARNING] No results to display.", file=sys.stderr)
            return
        print("\n=== Mutation Rate Results ===")
        print(self.results.to_string(index=True))
        print()

    def save(self, output_path: str) -> None:
        """
        Save the results DataFrame to a CSV file.

        Parameters
        ----------
        output_path : str
            Destination path for the CSV file.
        """
        if self.results is None:
            print("[ERROR] No results to save — run analysis first.", file=sys.stderr)
            return
        self.results.to_csv(output_path, index=False)
        print(f"[INFO] Results saved to: {output_path}", file=sys.stdout)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Parse arguments and run the mutation-rate analysis."""
    parser = build_parser()
    args = parser.parse_args()

    # ── 1. Parse the FASTA file ──────────────────────────────────────────────
    try:
        sequences = parse_fasta(args.fasta)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    # ── 2. --list-ids early-exit ─────────────────────────────────────────────
    if args.list_ids:
        print(f"Found {len(sequences)} sequence(s) in '{args.fasta}':")
        for seq_id in sequences:
            print(f"  • {seq_id}")
        sys.exit(0)

    # ── 3. Require --reference for the main analysis ─────────────────────────
    if not args.reference:
        print(
            "[ERROR] --reference is required unless --list-ids is used.\n"
            "        Run with --list-ids to see available sequence IDs.",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── 4. Run analysis ───────────────────────────────────────────────────────
    analysis = MutationRateAnalysis(
        fasta_path=args.fasta,
        reference_id=args.reference,
        ignore_gaps=not args.keep_gaps,
    )
    try:
        analysis.load()
        analysis.run()
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    analysis.display()

    # ── 5. Optionally save ────────────────────────────────────────────────────
    if args.output:
        analysis.save(args.output)


if __name__ == "__main__":
    main()
