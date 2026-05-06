
<!-- __Research Methods in Biomedical Informatics__\
__Programming Assignment__\
__Spring 2026__ -->

![tests](https://github.com/canderson318/research-methodology-programming-assignment/actions/workflows/tests.yml/badge.svg)

## Overview
This repo contains code that finds the longest contiguous sequence that contains a query sequence from a query sequence and fasta format file of next-gen sequencing reads.

*__Find the assignment description [here](assignment.md).__*\
*__Find the assignment report [here](deliverables/module-3/report/main.pdf).__*\
*__Find the final presentation recording [here](deliverables/module-3/presentation/recording.mp4).__*\

### Motivation
There are many applications wherein a researcher would like to know the sequence context around a given query sequence they suspect exists in their sample. For example, gene targeting may be used to create a knock-out model and the researcher would like to verify that the target vector was incorporated into the right place in the genome. Alternatively, a researcher might wish to fully identify suspected contaminating sequences that would indicate the presence and/or source of unclean sample handling procedures in the laboratory, such as a specific PCR primer contamination.

### Key Problem
Take as input the set of all next-generation sequencing reads identified in a sample and an initial query sequence, and return the largest sequence contig that can be constructed from the reads that contains the initial query sequence.

----

## Set up
Set up your conda environment using the environment file `environment.yaml`
```bash
conda env create -f environment.yaml
conda activate res-meth
```

## Usage

Below is an example execution for next-gen reads `READS.fasta` and a query sequence `QUERY.fasta` both in fasta format.

**Example directory tree:**
```
working_directory/
    src/
        main.py
        functions.py
    in/
        READS.fasta
        QUERY.fasta
    out/
```

**Example usage:**
```bash
cd working_directory
python -m src.main -k 32 --in_dir in/assigned --out_dir out/assigned --save_adjacency -t 3
```

**Arguments:**

| Argument | Flag | Type | Default | Description |
|---|---|---|---|---|
| kmer size | `-k` | `int` | required | Length of each k-mer fragment |
| input directory | `-i` / `--in_dir` | `str` | required | Directory containing `QUERY.fasta` and `READS.fasta` |
| output directory | `-o` / `--out_dir` | `str` | required | Directory to write results |
| save edge list | `-adj` / `--save_adjacency` | flag | `False` | Save k-mer edge list as `edge_list.pkl` |
| frequency threshold | `-t` / `--filter_threshold` | `int` | `1` | Remove k-mers with count ≤ this value |

_Note: higher values of `k` result in more unique k-mers and greater specificity, but require longer reads and higher coverage to maintain graph connectivity._

**Output**

Running `python -m src.main` creates three files in `out_dir`:

- `ALLELES.fasta` — fasta file of the top assembled contigs containing the query
- `ALLELES.aln` — tab-separated alignment table (see columns below)

`ALLELES.aln` columns:

| Column | Description |
|---|---|
| `sseqid` | Read name (from `READS.fasta`) |
| `qseqid` | Contig name (from `ALLELES.fasta`) |
| `sstart` | Start coordinate in read where alignment begins |
| `send` | End coordinate in read where alignment ends |
| `qstart` | Start coordinate in contig where alignment begins |
| `qend` | End coordinate in contig where alignment ends |

Example:

|`sseqid`|`qseqid`|`sstart`|`send`|`qstart`|`qend`|
|:--:|:--:|:--:|:--:|:--:|:--:|
|2S43D:08461:04180|contig1|13|40|1|64|
|2S43D:07701:07310|contig1|20|112|240|332|
|2S43D:07489:10315|contig1|123|90|20|53|
|2S43D:04035:14719|contig1|105|41|10|74|

---

## Testing

Unit tests cover core functions in `functions.py`. Run with:
```bash
python -m pytest src/tests/test_functions.py -v
```

Pipeline/integration tests are in `src/tests/test1.py`, `test2.py`, etc.

---

## Source Descriptions

#### `main.py`
Takes NGS reads and an initial query sequence, assembles the longest contig containing the query using a de Bruijn graph approach, and writes `ALLELES.fasta`, `ALLELES.tsv`, and `ALLELES.aln`.

#### `functions.py`
Helper functions:

- `load_data(in_dir)` → `dict`
  - Reads `READS.fasta` and `QUERY.fasta` from `in_dir` into a dictionary

- `parse(l: list)` → `(headers, sequences)`
  - Splits a fasta line list into header strings and sequence strings

- `segment(s: str, t: int)` → `Dict[str, List[Tuple[int, int]]]`
  - Returns all t-length substrings of `s` and their `(start, end)` positions; repeated k-mers accumulate all positions

- `segment_all(sequences: list[str], t: int)` → `(Counter, Dict[str, List])`
  - Applies `segment` across all sequences; returns k-mer frequency counter and per-k-mer read index mapping `{kmer: [(read_idx, [(start, end)])]}`

- `summarize(arr: NDArray)` → `dict`
  - Returns N, mean, sd, median, Q1, Q3 for a numeric array

- `seq_summary(sequences)` → `dict`
  - Applies `summarize` to sequence lengths

- `align(s1: str, s2: str)` → `bool`
  - Returns `True` if `s1` and `s2` overlap by k-1 chars (`s1[1:] == s2[:-1]`), i.e. `s1 → s2` is a valid de Bruijn edge

- `make_contigs(kmer_mapping: Dict, query: str, k: int, max_visits: int = 2)` → `(left_contigs, right_contigs, edge_list)`
  - Anchors on query k-mers and traverses the de Bruijn graph outward in both directions
  - `left_contigs`: list of k-mer paths extending left of the query
  - `right_contigs`: list of k-mer paths extending right of the query
  - `edge_list`: dict of `{kmer: (predecessors, successors, count)}`
  - `max_visits`: how many times a path may revisit the same k-mer before terminating (handles repeated sequence)

- `print_contig_with_context(contig, query, context)` / `print_contigs_with_context(...)`
  - Prints contig to terminal with query highlighted in blue and surrounding context

#### `assigned.py`
Runs `main.py` on the assigned dataset (`in/assigned/`) with preset parameters and plots the k-mer de Bruijn graph.

#### `simulate_reads.py`
Simulates reads from a known ground-truth sequence and writes them to fasta format for testing.