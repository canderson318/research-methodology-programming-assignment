__Research Methods in Biomedical Informatics__\
__Programming Assignment__\
__Spring 2026__\

__ __ __


## Key problem
There are many applications wherein a researcher would like to know the sequence context around a given query sequence they suspect exists in their sample. For example, gene targeting may be used to create a knock-out model and the researcher would like to verify that the target vector was incorporated into the right place in the genome. Alternatively, a researcher might wish to fully identify suspected contaminating sequences that would indicate the presence and/or source of unclean sample handling procedures in the laboratory, such as a specific PCR primer contamination.
Create a program that takes as input the set of all next-generation sequencing reads identified in a sample and an initial query sequence and returns the largest sequence contig that can be constructed from the reads that contains the initial query sequence.

#### Example
_Query sequence:_ <span style = "color:red">ZZZZZZZZZ</span>

|***Sequencer reads***|||
|:---------:|:---------:|:---------:|
|ZZZWZYZYY|<span style = "color:blue">YYYYY</span>VYYY|XXXXZZZZZ|
|<span style = "color:red">ZZZZZZZZZ</span>|<span style = "color:purple">XXXXXXXXX</span>|ZZZZY<span style = "color:blue">YYYYY</span>|
|BBBBZBBYB|BBBBXXZZY|DDDDDDDDD|

*Output contig:* <span style = "color:purple">XXXXXXXXX</span><span style = "color:red">ZZZZZZZZZ</span><span style = "color:blue">YYYYYVYYY</span>


#### Usage
<u>Input:</u>
- QUERY.fasta : fasta file containing initial query sequence (size: 1 KB)
- READS.fasta.gz : gzipped fasta file of sequencer reads (size 5 MB, gunzip before use)
Note: The files provided are data from a real sequencing run, with all inherent errors and artifacts.

<u>Output:</u>
- `ALLELES.aln` : tab-delimited text file describing alignment of sequence reads to contig(s) in
- `ALLELES.fasta` : fasta file of the largest constructed contig (allele) containing the initial query

- `ALLELES.tsv` the with the following columns (see example further below):

	- `sseqid`
		+ name of sequencing read (from READS.fastq.gz)

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

Coordinates should respect that the contig in `ALLELES.fasta` is in the forward orientation, such that if the sequencing read sseq aligns in the forward direction with respect to the contig, send > `sstart`, whereas if sseq aligns in the reverse direction with respect to the contig, send < `sstart` (in italics below). It is not necessary to include identifiers for sequences from READS.fastq.gz that do not align to the sequence in `ALLELES.fasta`. Additional informative columns may be added to the text file, as you deem useful or appropriate.

Example output.aln file:

|`sseqid`|`qseqid`|`sstart`|`send`|`qstart`|`qend`|
|:--:|:--:|:--:|:--:|:--:|:--:|
|2S43D:08461:04180|contig1|13|40|1|64|
|2S43D:07701:07310|contig1|20|112|240|332|
|2S43D:07489:10315|contig1|123|90|20|53|
|2S43D:04035:14719|contig1|105|41|10|74|
_ _ __ _ _
## Deliverables
### Module 1
- A short (max 10 minute) pre-recorded presentation that includes:
    - a clear and concise problem statement and algorithm design description that is targeted at a general scientific audience. Figures such as flow charts and schematics are encouraged.
Technical jargon is discouraged.
    - a detailed development and testing plan that is targeted at a fellow methods developer. This plan should explain how you will decompose your solution into independent modules, how those
modules will interact, how they will be tested, and a timeline.
### Module 2
- A well documented and organized GitHub repository.
- A written report containing
	- An update on the proposed timeline
	- Full write ups of completed components. These sections should include details on the solutions and analysis of results.
	- Stubs for partially completed components
### Module 3
- A well documented and organized GitHub repository.
- A complete written report.
- A short (max 10 minute) pre-recorded presentation that includes a clear and concise problem statement
and algorithm design description and results that is targeted at a general scientific audience. Figures
such as flow charts and schematics are encouraged. Technical jargon is discouraged.

### Grading
You will be graded on the following four standards. Each standard has between 1 and 3 assessments. Each
assessment will be assigned between a 1 (no or minimal attempt) and 4 (publication quality). To master a
standard you must score a 3 or 4 on each assessment. There is no limit to the number of times you can
attempt an assessment. Reattempting an assessment requires a non-trivial written justification that details
what went wrong in prior assessment and what steps were taken to correct those issues.

1.​ Oral communion
- Module 1 presentation
- Module 3 presentation

1.​ Written communication
- GitHub `README`
- Module 2 report
- Final report

1.​ Algorithm design
- Module 1 presentation
- Module 2 presentation
- Final report

1.​ Source code
- GitHub repo

To get an A you must master all four standards. For a B you must master 3, and a C requires 2.
_ _ __ _ _
## Programming languages and libraries
You are free to choose whatever programming language you like, but in general you may not use any bioinformatics toolkits or libraries. You are allowed to use libraries for calculation of common statistical tests and p-values (like t-test, Wilcoxon, Kolmogorov Smirnoff, etc), but you must fully cite the source. If there is any question about the eligibility of a specific statistical test, do not hesitate to mail ryan.layer@colorado.edu. Also, if you are programming in C++, the use of the Standard Template Libraries is allowed. If you are programming in python, you may use scipy and the numpy multidimensional array library. If there are questions, please send an email to ryan.layer@colorado.edu; reasonable accommodations will be made with the goal of standardizing available data structures across languages that students may choose.
_ _ __ _ _
## GitHub repository
Your GitHub repository will likely be visited more often than its associated publication, and the impact of your software will depend on how well your repository is organized. In addition to organizing your code in folders, making the `README` legible and useful is critical. GitHub markdown makes formatting easy, and at a minimum your `README` needs to have:
- A short description of what your project does.

- This is your elevator speech in text form. Keep it brief and mention relevant information which could include the relevant scientific field, statistical models, and input data. Think of the description as an abstract to the software, which can be more specific than the research abstract in some areas and more general in others.

- How to use your project, with examples. 

- This section can include the usage that is produced by argparse, but needs to go into much more detail with specific examples. Go into detail about the format of input files, and give different combinations of input parameters and the resulting software behavior.

- How to install the software.

- You can never take for granted user system configurations, so give a step-by-step guide thatgives specific commands to install all dependencies and run all tests. Conda is useful here because it gives a common starting point.

<small>
<center>
For more on this topic please visit <span style = 'color:skyblue'> https://dbader.org/blog/write-a-great-readme-for-your-github-project</span>
</center>
</small>

_ _ __ _ _

## Pre-recorded presentations
For these assignments, imagine that you are giving a talk at the American Society of Human Genetics meeting, or a similarly large conference with diverse attendees. Given the wide range of scientific backgrounds in your audience, the vast majority of which are not method developers. You must clearly and convincingly motivate the problem and your proposed solution without relying on jargon. Visual aids can effectively support your argument, but they can also be a distraction. Consider every line in your visuals and every word in your description and how they contribute to supporting your argument. If they can be removed without hurting the argument, then do so. The exception is in module one where I ask you to give a development and testing plan. Treat this as a distinct presentation where I am specifically asking for technical details.

## Written report
​The written report should describe and justify your strategy, define the input files, present the algorithm overview, define any scoring methods, and detail the expected output files. The report should also contain an analysis of the final results and discussion. You should cite the appropriate scientific literature where appropriate.

## Testing
Testing is critical to robust and reproducible scientific research software. Integrating testing into your software design and development process (vs adding tests at the end) promotes abstraction and modularization. I expect your design plan to include testing plans for each component of your project and for the final code base to be thoroughly tested. In Python, unit tests are an easy and fast testing strategy.
