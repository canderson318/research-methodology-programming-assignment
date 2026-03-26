/*
#---- sync results to this directory
cd /Users/canderson/Documents/school/res-meth-class/programming-assignment/deliverables/module-2
rsync -a --progress --ignore-times /Users/canderson/Documents/school/res-meth-class/programming-assignment/versions/version002/out out
*/

#import "utils.typ": *
#import "@preview/zebraw:0.6.1": *
#show: zebraw

////////////////////
// Document Settings
////////////////////
#set page(margin: 1in, width: 8.5in, height: 11in, numbering: "1")
#let fntsz = 10pt
#let after = fntsz * 1.5
#set text(font: "Georgia", size: fntsz)
#set par(leading: fntsz, spacing: after)
#set heading(numbering: "1.")

////////////////
// Set Defaults
////////////////

#show math.equation: set text(size: 12pt)

#show title: it => {
  set align(center + horizon)
  set text(size: 20pt, weight: "bold")
  v(-5em)
  it
}

#show outline: it => {
  show heading: set text(size: 15pt)
  show outline.entry: it => pad(left: 1em, right: 0em, it)
  it
}

#show link: it =>{
    set text(blue)
    it
}

#show ref: it =>{
    set text(style:"italic")
    it
}

#show heading: it=>{
    block(below:after)[#it]
}

#show figure.where(kind: "code"): it => {
    // let col = rgb("#2746e397")
    // block(fill: none, stroke: col, inset: 8pt,below:5pt, radius: 20pt, width: 100%)[
    //     #it.body
    // ]
    block[
        #it.body
    ]
    v(-1em)
    it.caption
}


//////////////////////
//////////////////////
//////// BODY ////////
//////////////////////
//////////////////////

#title[Next-Gen Read Alignment and Contig Query Identification]
#align(center)[By: Christian Anderson\ #today.display("[day] [month repr:long] [year]")]
#let gh = link("https://github.com/canderson318/research-methodology-programming-assignment")[GitHub]
#align(center)[#gh]

#align(bottom, outline())
#pagebreak()


= Timeline
My goals for the second module of this project were as follows: 
#emph[
  - Brainstorm Algorithm #sym.checkmark
    - Research De Brujin Graphs #sym.checkmark
  - Develop program #sym.checkmark
    - Load Data #sym.checkmark
    - Parse fastas into workable python objects #sym.checkmark
    - Fragment reads into kmers #sym.checkmark
      - Save kmer read ids #sym.checkmark
    - Filter Kmers #sym.checkmark
    - Make directed graph #sym.checkmark
      - Connect similar kmers #sym.checkmark
        - make adjacency matrix where k-1 overlap #sym.checkmark
    - Make contigs #sym.checkmark
      - Traverse every path from some set of starting nodes #sym.checkmark
      - Construct contig along the way #sym.checkmark
      - #strong[Save contigs containing query sequence]
  - Create a #gh repo #sym.checkmark
]
Since my initial brainstorming for this project summarized in my Module-1 talk, I have completed nearly all of my goals (checkmarked, #sym.checkmark). I still need to identify contigs containing the query sequence due to my code's current limitations (@nextsteps).

= Findings
Here I go in to depth outlining my approach to find the longest contig containing a query sequence. As of yet, I do not have results but I have learned a lot and have much to improve on. 

== Read Alignment
The first steps of loading and parsing the fastas was trivial, but fragmenting the kmers was slightly more complicated as I wanted a way to encode read frequency and provenance (their parent read). A python ```python Counter()``` was perfect for this as it records the kmer string as well as how many times it was observed. Within the counter loop, I fragment each read into `k`<k> length words, _mers_, using a stride of one character at a time:
#align(center)[
    #block(align(left)[
        $"for" i in [ 1, |"string"|-k], "do"\
        space space space space"kmer"_(i) = "string"(i, i+k)\
        space space space space"count" "kmer"_i\
        space space space space"record read id"\
        "end for" $
    ])
]

For example with the following string a k of 3:\
#align(center)[$"thequickbrownfox" -> "the"_(i = 1), "heq"_(i = 2), "equ"_(i = 3), "qui"_(i = 4), "uic"_(i = 5), ... "fox"_(i = (|"string"| - k) ) $]

To record kmer provenance, I just ran the kmer counter alongside a dictionary for each kmer which saved the read id and its coordinates in that read which I pass on to the final results. I then took this set of strings and their frequencies and kept ones observed more than once.

The next step was to encode relationships of overlap between these kmers. I accomplished this by looping over every $i , j$ combination of kmers, recording their k-1 overlap in an adjacency matrix, $A$. 

#align(center)[
  $(A)_(i j) = cases(
    1 "if" "kmer"_(i)(2:k) space equiv space "kmer"_(j)(1:k-1),
    0 "if" "kmer"_(i)(2:k) space equiv.not space "kmer"_(j)(1:k-1)
  ) "for" i != j$
]

The adjacency matrix, $A$, is the matrix representation of a graph that encodes how each kmer overlaps or doesn't overlap with every other kmer: if for a element with a value greater than zero, that means there is an edge between the column and row kmer. And because I compared every $"ith"$ to every $"jth"$ string, each pair of kmers is compared two times, one time A to B and again B to A. This makes the graph directional which is important because DNA is directional, so edges lying below the diagonal ($(A)_(i<j) < 1$) means the 2-length contig reads $"kmer"_i->"kmer"_j$ and edges in the upper diagonal read $"kmer"_j->"kmer"_i$.

#strong[Contiguous Sequence Creation] \
To reiterate this project's primary task, I need to find the DNA sequence containing a query sequence from fragments of DNA. At this point I knew where each kmer came from and how each one overlapped with every other, but translating that overlap information into an actual assembled sequence remained the core challenge. To find the largest contiguous sequence (contig) containing the query sequence requires traversing every possible path through the graph which quickly becomes NP-hard as each step through the graph spawns even more possible paths.

For example, a fully connected graph containing only 10 nodes, $P$, has
$(P-2)!e = 1.10*10^5$ //https://math.stackexchange.com/questions/2406920/total-number-paths-between-two-nodes-in-a-complete-graph
different possible paths from each node to every other node.
When I processed the assigned 124,520 reads to a kmer length of 120, I was left with 2,734,978 unique kmers. This number luckily reduces down to 14,758 when keeping only kmers observed more than three times, but even with a fraction of the total possible kmer count, assuming the graph is fully connected, there would be essentially infinite possible paths from each node to every other (approx. $5.89*10^55111$). That being said, it was critical that my pipeline reduce the search space and that my algorithm be both memory efficient and fast.

My first idea was to use a recursive algorithm that looks at the next connected nodes for each node, setting each next node as the current, and so on. I set it to loop over nodes with the fewest incoming edges ($arg min("colsum"(A))$) and build contiguous sequences from there, keeping track of visited nodes so it didn't get caught in cycles. This approach worked well on test data, but quickly reached recursion limits with the actual assigned data. Recursive algorithms are also mind bending (at least for me), especially when debugging, so I instead used a iterative approach where the algorithm continues searching while possible. This method explores branches in a similar manner (depth first), but it makes the current states more observable, which is preferable for debugging. I'll go through its steps in more depth.

== Main Algorithm

#figure(caption:[Defining functions and formating initial conditions.], kind: "code", supplement: [Code])[
```python
def make_contigs_from_adj(query, adj):
    def _get_starts(adj):
        col_sums = adj.sum(0)
        return np.argwhere(col_sums == col_sums.min()).ravel().astype(np.int32)
    def _get_nexts(curr):
        return np.argwhere(adj_np[curr, :] > 0).ravel().astype(np.int32)
    def _save(contig):
        """check if contig inds contain teh query string, if so save"""
        # append last char consecutively
        string = construct_string_from_debrujin(str_index, contig)
        if query in string:
            contig_arr = np.array(contig)
            contig_res.append((string,contig_arr))

    str_index = adj.columns.values
    adj_np = (adj > 0).to_numpy().astype(np.int8)
    starts = _get_starts(adj_np)
    contig_res = []
``` ]<start>

The function accepts a `query` and `adj` argument. I made the addition of the query to allow for more dynamic contig creation; because we only care about contigs with the query, the funtion only returns those.

I first define some functions:
- ```python _get_starts()``` finds the starting nodes `starts` which are the indices of the minimum adj colsums.
- ```python _get_nexts()``` finds the next nodes which are the indices of where a current nodes values are greater than 0.
I then converted the adjacency matrix `adj` from a pandas ```python DataFrame()``` to a 8-bit binary numpy matrix to save memory, find the `starts` nodes, and define an empty list to save results. \

#figure(caption:[Creating contigs while walking through graph.], kind: "code", supplement: [Code])[
```python
for start in starts:
    states = [(start, [start], {start})]
    while states:
        current, contig, visited = states.pop() 
        nxts = _get_nexts(current)
        if len(nxts) == 0:
            _save(contig)
            continue
        for nxt in nxts:
            if nxt in visited:
                _save(contig)
                continue
            states.append((nxt, contig + [nxt], visited | {nxt}))
```]<loop>

Next, I enter the meat of the algorithm where contigs grow as new nodes are visited. \
Here I utilize a stack, `states`, which grows and shrinks as branches grow, terminate, or are saved. The stack saves the current node in the walk, `start`, the current walk, `[start]`, and the nodes visited along the walk, `{start}`, for all traversed paths from a starting node. 
The loop begins with `start` in each slot of the state list and then builds that list while `states` is non-empty. For each iteration within the while loop, the most recent (aka, rightmost/topmost) state in the stack is assigned to respective objects and removed from list in the same line once using the ```python pop()``` function. This current node is now being built off of using the `contig` list, so long as there are connected nodes and they are unvisited. If a `nxt` node has been visited or if there are no outgoing edges from the current node, ```python _save()``` will save the contig string and it's indices (kmer ids) to the `contig_res` list only if the query string is in that contig. If there are more `nxt` nodes to visit from the current node, a new state is added to the top of the stack with `nxt` taking the `current` place, `contig` += `nxt` taking the place as contig, and `visited` += `nxt` taking the place of the `visited` slot (@loop, line 13). Here is the critical point where contigs grow as new nodes are visited until there are no more to visit. The stack `states` is constantly growing and shrinking; growing as many `nxt` nodes are visited, and shrinking each time the stack is popped and the contig saved. 

This runs for all `starts` and then returns the `contigs_res` list with the following structure:

```
list[ tuple[ string[<contig>], array[<kmer_indices>] ] ]
```
#emph[The full algorithm can be found in @algcode.]

= Conclusions, Thoughts, and Next Steps <nextsteps>
I've poured 100% effort into the first 90% of this project, therefore last 10% should only cost me 1,000% of my effort. Nevertheless, the most daunting step of designing a graph search algorithm is for the most part completed and the mostly entails playing around with parameters and optimizing the code. 

I need to find the sweet spot for the $k$ parameter because as k increases, the number of unique kmers increases as well. To illustrate this, I ran my algorithm twice on the assigned reads. There are 1,008,559 unique 10-mers which reduces down to 810,182 after filtering out uncommon kmers ($"count"<3$) and 2,734,978 unique 120-mers which reduces down to 14,758 after the same filtering. So, as $k$ increases, raw kmer count increases but filtered kmer count decreases. That means I need to gauge the filtering threshold inversely to $k$ and find the region of $k$ and $t$ values that has enough granularity for the query to be findable and computationally feasible.

I am also not utilizing the query to reduce the search space. I could be subsetting the graph for nodes connected to the query's kmers. Starting at the last kmer in the query, I can then branch out from there for every next node to build the kmer from the positive end. I can also branch the other direction to build from the negative end. This approach should not take too much to implement into my existing code and should reduce runtime significantly.  

As of right now I calculate an adjacency matrix which is major memory hog. I can try using a dictionary approach to measure each node's preceding and next nodes. Using this should be just as easy and fast as the adjacency matrix to look up the next and preceding kmers without as much overhead. 

= Updated timeline

- Build code (+2 weeks)
    - Optimize code by trying query search cheat
    - Try the dictionary approach to speed up graph search
    - Connect kmers to reads, kmers to contigs, contigs to reads
    - Find the longest contigs with the query sequence
- Find longest contig (+1 weeks)
    - Optimize filtering threshold and k parameters 
        - Do simple grid search to find right pair
        - Identify simple heuristic for for k and t by trying gridsearch on simulated data
- Finalize GitHub (1 day)
- Complete report (2 days)
- Final presentation (4 days)




#pagebreak()
= Algorithm Code <algcode>

For all codes visit my #gh.

#strong[Code]
```python
def construct_string_from_debrujin(kmers:NDArray, inds: NDArray):
    """Construct continuous string for debrujin graph path, appending every last character to string"""
    string = kmers[inds[0]] 
    for ind in inds[1:]:
        string+=kmers[ind][-1]
    return string

def make_contigs_from_adj(query, adj):
    def _get_starts(adj):
        col_sums = adj.sum(0)
        return np.argwhere(col_sums == col_sums.min()).ravel().astype(np.int32)
    def _get_nexts(curr):
        return np.argwhere(adj_np[curr, :] > 0).ravel().astype(np.int32)
    def _save(contig):
        """check if contig inds contain teh query string, if so save"""
        # append last char consecutively
        string = construct_string_from_debrujin(str_index, contig)
        if query in string:
            contig_arr = np.array(contig)
            contig_res.append((string,contig_arr))

    str_index = adj.columns.values
    adj_np = (adj > 0).to_numpy().astype(np.int8)
    starts = _get_starts(adj_np)
    contig_res = []

    for start in starts:

        states = [(start, [start], {start})]

        while states:
            # get current states
            current, contig, visited = states.pop() # take the last element of the list ( a tuple )
            nxts = _get_nexts(current)

            if len(nxts) == 0:
                _save(contig)
                continue

            for nxt in nxts:
                if nxt in visited:
                    _save(contig)
                    continue
                # update states pushing forward through tree
                #++ current:=nxt, contig:= contig+[nxt], visited:= visited + nxt
                #++ each item of states is a tuple encoding the [current, extending branch, and visited nodes]
                states.append((nxt, contig + [nxt], visited | {nxt}))

    return contig_res

```

// #pagebreak()
// #text(red)[
//   - A well documented and organized GitHub repository.
//   - A written report containing
//     - An update on the proposed timeline
//     - Full write ups of completed components. These sections should include details on the solution - and analysis of results.
//     - Stubs for partially completed components
// ]

// typst compile main.typ
// git add main.pdf
// git commit -m  "Recompile report"
// git push