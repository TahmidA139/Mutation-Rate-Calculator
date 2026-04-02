# Mutation-Rate-Calculator

A command-line tool that reads a multiple-sequence alignment (FASTA format) and computes the **mutation rate** of each sequence relative to a user-chosen reference, using **Pandas** for tabular output.

---

## Features

- Parses standard FASTA alignment files (`.fa`, `.fasta`, `.txt`)
- Validates that all sequences share the same aligned length
- Computes per-sequence: total sites, mutations, mutation rate, and percent identity
- Optional gap inclusion/exclusion (`--keep-gaps`)
- Saves results to CSV (`--output`)
- Graceful error handling with informative messages on `stderr`

---

## Project Structure

```
mutation_rate_calculator/
├── main.py              # Entry point — CLI + MutationRateAnalysis class
├── example.fasta        # Example aligned FASTA file for testing
├── run_tests.sh         # Bash script that exercises all features
├── README.md            # This file
├── LICENSE              # MIT License
└── mut_calc/            # Local package
    ├── __init__.py
    ├── fasta_parser.py  # FASTA parsing and validation
    └── mutation_rate.py # Mutation-rate computation + Pandas table builder
```

---

## Requirements

- Python ≥ 3.10 (uses `dict[str, str]` and `X | Y` union hints)
- [pandas](https://pandas.pydata.org/) — `pip install pandas`

Install in an Anaconda environment:

```bash
conda activate your_env
pip install pandas
```

---

## Usage

### List sequence IDs in a FASTA file

```bash
python main.py --fasta example.fasta --list-ids
```

### Run the analysis (gaps ignored by default)

```bash
python main.py --fasta example.fasta --reference "Reference_seq"
```

### Include gap characters in the mutation count

```bash
python main.py --fasta example.fasta --reference "Reference_seq" --keep-gaps
```

### Save results to CSV

```bash
python main.py --fasta example.fasta --reference "Reference_seq" --output results.csv
```

---

## Example Output

```
[INFO] Loading alignment from: example.fasta
[INFO] 6 sequences found.
[INFO] Reference sequence: Reference_seq

=== Mutation Rate Results ===
   sequence_id  total_sites  mutations  mutation_rate  percent_identity
0     Sample_D          120          3       0.025000           97.5000
1     Sample_E          119          3       0.025210           97.4790
2     Sample_B          120          2       0.016667           98.3333
3     Sample_C          120          2       0.016667           98.3333
4     Sample_A          120          0       0.000000          100.0000
```

---

## Running the Tests

```bash
bash run_tests.sh
```

This script tests: listing IDs, mutation-rate calculation, CSV output, and all error-handling paths.

---

## License

MIT — see `LICENSE` for details.
