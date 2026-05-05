# Module 3

## Assignment
- A well documented and organized GitHub repository. 
- A complete written report. 
- A short (max 10 minute) pre-recorded presentation that includes a clear and concise problem statement and algorithm design description and results that is targeted at a general scientific audience. Figures such as flow charts and schematics are encouraged. Technical jargon is discouraged. eted components

----

#### GitHub repository 
Your GitHub repository will likely be visited more often than its associated publication, and the impact of your 
software will depend on how well your repository is organized. In addition to organizing your code in folders, 
making the README legible and useful is critical. GitHub markdown makes formatting easy, and at a minimum 
your README needs to have: 
- A short description of what your project does. 
- This is your elevator speech in text form. Keep it brief and mention relevant information which 
could include the relevant scientific field, statistical models, and input data. Think of the 
description as an abstract to the software, which can be more specific than the research 
abstract in some areas and more general in others. 
- How to use your project, with examples. 
- This section can include the usage that is produced by argparse, but needs to go into much 
more detail with specific examples. Go into detail about the format of input files, and give 
different combinations of input parameters and the resulting software behavior. 
- How to install the software. 
- You can never take for granted user system configurations, so give a step-by-step guide that 
gives specific commands to install all dependencies and run all tests. Conda is useful here 
because it gives a common starting point. 

 
### Pre-recorded presentations 
For these assignments, imagine that you are giving a talk at the American Society of Human Genetics meeting, or a similarly large conference with diverse attendees. Given the wide range of scientific backgrounds in your audience, the vast majority of which are not method developers. You must clearly and convincingly motivate the problem and your proposed solution without relying on jargon. Visual aids can effectively support your argument, but they can also be a distraction. Consider every line in your visuals and every word in your description and how they contribute to supporting your argument. If they can be removed without hurting the argument, then do so. 
 
### Written report 
The written report should describe and justify your strategy, define the input files, present the algorithm overview, define any scoring methods, and detail the expected output files. The report should also contain an analysis of the final results and discussion. You should cite the appropriate scientific literature where appropriate. 
 
### Testing 
Testing is critical to robust and reproducible scientific research software. Integrating testing into your software design and development process (vs adding tests at the end) promotes abstraction and modularization. I expect your design plan to include testing plans for each component of your project and for the final code base to be thoroughly tested. In Python, unit tests are an easy and fast testing strategy. 