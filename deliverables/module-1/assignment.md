<!-- 

dir=/Users/canderson/Documents/school/res-meth-class/programming-assignment/deliverables/module-1
F=$dir/assignment.md
new_F=${F%.md}.pdf

cd $dir || exit 1

CMD="pandoc $F 	-f markdown -t pdf 	-o $new_F"

when-changed $F -c $CMD

 -->

# Module 1
- A short (max 10 minute) pre-recorded presentation that includes:
	- a clear and concise problem statement and algorithm design description that is targeted at a general scientific audience. Figures such as flow charts and schematics are encouraged.
	- Technical jargon is discouraged.
	- a detailed development and testing plan that is targeted at a fellow methods developer. This plan should explain how you will decompose your solution into independent modules, how those modules will interact, how they will be tested, and a timeline. 

## Grading
You will be graded on the following four standards. Each standard has between 1 and 3 assessments. Each
assessment will be assigned between a 1 (no or minimal attempt) and 4 (publication quality). To master a
standard you must score a 3 or 4 on each assessment. There is no limit to the number of times you can
attempt an assessment. Reattempting an assessment requires a non-trivial written justification that details
what went wrong in prior assessment and what steps were taken to correct those issues.

1. Oral communion
	- Module 1 presentation
	- Module 3 presentation
2. Written communication
	- GitHub README
	- Module 2 report
	- Final report
3. Algorithm design
	- Module 1 presentation
	- Module 2 presentation
	- Final report
4. Source code
	- GitHub repo

