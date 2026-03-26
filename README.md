
<!-- __Research Methods in Biomedical Informatics__\
__Programming Assignment__\
__Spring 2026__ -->

## Overview
This repo contains code that finds the longest contiguous sequence that contains a query sequence from a query sequence and fasta format file of next-gen sequencing reads.

*__Find the assignment description [here](assignment.md).__*
*__Find the assignment report [here](deliverables/module-2/report/main.pdf).__*

### Motivation
There are many applications wherein a researcher would like to know the sequence context around a given query sequence they suspect exists in their sample. For example, gene targeting may be used to create a knock-out model and the researcher would like to verify that the target vector was incorporated into the right place in the genome. Alternatively, a researcher might wish to fully identify suspected contaminating sequences that would indicate the presence and/or source of unclean sample handling procedures in the laboratory, such as a specific PCR primer contamination.

### Key Problem
Take as input the set of all next-generation sequencing reads identified in a sample and an initial query sequence, and return the largest sequence contig that can be constructed from the reads that contains the initial query sequence.

----

## Set up 
Set up your conda environment using the environment file `environment.yaml`
```bash
conda env create -f environment.yaml
```

## Usage

Below is an example execution for next-gen reads `reads.fasta` and a query sequence `query.fasta` both in fasta format. 
**Example directory tree:**
```raw
working_directory/
	- src/
		- main.py
		- functions.py
	- in/
		- reads.fasta
		- query.fasta
	- out/
```
**Example usage:**
```bash
cd working_directory
./src/main.py -k 10 --in_dir input/directory --out_dir output/directory --save_adjacency -t 10
```
**Arguments:**
`k`: the number of letters in each `k`mer read fragment.
_Note: higher values of `k` result in a greater quantity of unique kmers, this can become unwieldly very quickly._ \

`in_dir`: directory including `QUERY` and `READS` fasta files. 

`out_dir`: directory where results are saved. 

`save_adjacency`: the adjacency matrix of the  graph encoding kmer connections. 

`t`: the kmer frequency filtering threshold. Kmers with counts < `t` are removed from the graph. 

**Output**
Running `./src/main.py` will create three files in the `output` directory:

- `ALLELES.aln` : tab-delimited text file describing alignment of sequence reads to contig(s) in `ALLELES.fasta`
- `ALLELES.fasta` : fasta file of the largest constructed contig (allele) containing the initial query

- `ALLELES.tsv` the with the following columns (see example further below):

	- `sseqid`
		+ name of sequencing read (from reads.fastq)

	- `qseqid`

		+ name of contig matched (from ALLELES.fasta)

	- `sstart`

		+ starting coordinate in sequencing read `sseqid` that matches qseq

	- `send`

		+ ending coordinate in sequencing read `sseqid` that matches qseq

	- `qstart`
		+ starting coordinate in contig that matches sseq

	- `qend`
		+ ending coordinate in contig that matches sseq


Example output.aln file:

|`sseqid`|`qseqid`|`sstart`|`send`|`qstart`|`qend`|
|:--:|:--:|:--:|:--:|:--:|:--:|
|2S43D:08461:04180|contig1|13|40|1|64|
|2S43D:07701:07310|contig1|20|112|240|332|
|2S43D:07489:10315|contig1|123|90|20|53|
|2S43D:04035:14719|contig1|105|41|10|74|


## Source Descriptions

#### `main.py`
- Takes next-generation sequencing reads identified in a sample and an initial query sequence and returns the largest sequence contig that can be constructed from the reads that contains the initial query sequence

#### `functions.py`
- Contains helper functions
	- `load_data`
		- reads fasta files into a dictionary
	- `parse`
		- separates fasta sequences and headers of a list of fasta lines
	- `segment`
		- count each kmer 
	- `segment_all`
		- wrapper to apply segment to all sequences in a list
	- `summarize`
		- calculate stats (e.g. mean, sd) of an array
	- `seq_summary`
		- `summarize` string lengths
	- `align`
		- check if two strings match  
	- `make_adj`
		- make adjacency matrix between every combination of strings in Counter where matches fill matrix with a 1, and non-matches a 0 
	- `make_contigs`
		- take an adjacency matrix from `make_adj` and iteratively following all possible paths through it, appending contigs along the way

#### `simulate_reads.py`
- Simulates random reads of a specific length and writes these to a fasta format including the ground truth sequence

#### `assigned.py` 
- Script where args are formatted into `main.py` to query reads.