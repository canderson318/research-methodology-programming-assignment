/*
ROOT=/Users/canderson/Documents/school/res-meth-class/programming-assignment
RELPATH=deliverables/module-3/presentation
cd $ROOT/$RELPATH/images/ && ./process-images.sh || exit 1
cd $ROOT || exit 1
typst compile --root $ROOT  $RELPATH/main.typ


typst watch --root $ROOT  $RELPATH/main.typ


open deliverables/module-3/presentation/main.pdf


*/

#import "lib.typ": *

#let theme_col= rgb("5a0d87")
#let foot_col= red

#show footnote.entry: set text(foot_col,size:.8em)

#show footnote: it => (
    context {
      text(fill: foot_col, size: 1.2em)[#it]
    }
  )

#show figure.caption: emph

// Project configuration
#show: typslides.with(
  ratio: "16-9",
  theme: theme_col,
  font: "Fira Sans",
  font-size: 20pt,
  link-style: "color",
  show-progress: true,
)

#front-slide(
  title: "Next-Gen Read Alignment and Contig Query Identification",
  subtitle: "Research Methods in Biomedical Informatics",
  authors: "Christian Anderson",
  info: today.display( "[day] [month repr:long] [year]"),
)

#table-of-contents()


#title-slide[Background]



#slide(title: "Problem", outlined: false)[
  Imagine you want to confirm that a mutation is present in a mouse model of brittle bone disease. You have millions of short DNA fragments from a sequencer and one short sequence you know should be there. How do you find the full surrounding region?

  #v(1em)
  - Researchers validating transgenic knock-in models need to confirm the sequence around a mutation
  - There is no reference to compare against
  - All you have is the sequence you are hoping was knocked in
]

#slide(outlined: false)[
  #framed(title: "Problem")["Create a program that takes as input the set of all next-generation sequencing reads identified in a sample and an initial query sequence and returns the largest sequence contig that can be constructed from the reads that contains the initial query sequence."]
]


#slide(title: "DNA sequencing produces fragments, not full genomes", outlined: false)[
  Genomes can be billions of base pairs long, but sequencing machines can only read hundreds to thousands at a time. 
  
  The genome must first be shattered into millions of small fragments, each sequenced independently, then computationally reassembled.

  #v(.5em)
  #set align(center)
  #grid(columns: (1fr, 1fr), gutter: 20pt,
    framed(back-color: white)[
      *Short reads (Illumina)*\
      150 bp · very accurate\
      Struggles with repetitive regions
    ],
    framed(back-color: white)[
      *Long reads (PacBio, Oxford Nanopore)*\
      10,000+ bp · less accurate\
      Spans repetitive regions
    ]
  )
]





#slide(outlined: false)[
  #place(horizon+center)[#framed[
    #set align(left)
    Query sequence: #text(red)[ZZZZZZZZZ]

    Sequencer reads:\
    #table(
    columns: (auto, auto, auto),
    inset: 10pt,
    align: horizon,
      [ZZZWZYZYY], [#text(blue)[YYYYY]VYYY],[#text(purple)[XXXX]#text(red)[ZZZZZ]],
      [#text(red)[ZZZZZZZZ]],[#text(blue)[XXXXXXXXX]],[#text(red)[ZZZZ]#text(blue)[YYYYY]],
      [BBBBZBBYB],[BBBBZBBYB],[DDDDDDDDD],
    )

    Output contig: #text(purple)[XXXXXXXXX]#text(red)[ZZZZZZZZZ]#text(blue)[YYYYY]VYYY
  ]]
]

#slide(outlined: false)[
  #grid(columns:(2fr,1fr,2fr), gutter: 10pt,
    [#align(center)[#image("images/shredded-newspaper.jpg", height: 200pt, fit:"contain")]],
    [#text(5em,theme_col)[#align(center)[$arrow.r$]]],
    [#align(center)[#image("images/reconstructed-newspaper.jpg", height: 200pt, fit:"contain")]],
  )
]

#let sl(overlay:none)= slide(title:"What are kmers?", outlined: false)[

  #set align(top+center); 
  #set text(size: .8em)
  #framed(back-color: white)[
    "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort."\
    \–_The Hobbit_@tolkien2012hobbit
  ]
  #overlay

]

#sl()

#sl(overlay:[
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Remove non-alphanumeric characters]])
  #framed(back-color: white)[inaholeinthegroundtherelivedahobbitnotanastydirty...]
])

#sl(overlay:[
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Remove non-alphanumeric characters]])
  #framed(back-color: white)[inaholeinthegroundtherelivedahobbitnotanastydirty...]
  #block(inset:(x:0cm,y:0cm),height:0cm, fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Simulate Reads by taking random substrings of different length]])
  #framed(back-color: white)[#align(left)[inahole\ intheground\ edahobbitno\ itnotanastydirty ...]]
  ])

#sl(overlay:[
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Remove non-alphanumeric characters]])
  #framed(back-color: white)[inaholeinthegroundtherelivedahobbitnotanastydirty...]
  #block(inset:(x:0cm,y:0cm),height:0cm, fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Simulate Reads by taking random substrings of different length]])
  #framed(back-color: white)[#align(left)[inahole\ intheground\ edahobbitno\ itnotanastydirty ...]]
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Chop into $k$ length 'mers using a sliding window]])
  #framed(back-color: white)[#align(left)[$k = 5$\ inaho, nahol, nahole, aholei, holein, ... itnot, tnota, notan, otana ...]]
  ])

#sl(overlay:[
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Remove non-alphanumeric characters]])
  #framed(back-color: white)[inaholeinthegroundtherelivedahobbitnotanastydirty...]
  #block(inset:(x:0cm,y:0cm),height:0cm, fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Simulate Reads by taking random substrings of different length]])
  #framed(back-color: white)[#align(left)[inahole\ intheground\ edahobbitno\ itnotanastydirty ...]]
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Chop into $k$ length 'mers using a sliding window]])
  #framed(back-color: white)[#align(left)[$k = 5$\ inaho, nahol, nahole, aholei, holein, ... itnot, tnota, notan, otana ...]]
  #place(bottom+right,dx:2cm, dy:-2cm)[#block(inset:(x:1cm,y:1cm), fill: none,radius:.2cm,[#set text(1.5em,fill: red);#strong[How do we work backwards?] ])]
  ])


#slide(title:"What is a graph?", outlined:false)[
 #text(.9em)[#align(top)[A graph is a structure used to encode connections between things.]]
 #text(size:.5em)[ #figure(image("images/simple-graph.png", width: auto, height: 60%, fit:"contain"), caption: [A simple graph used to represent how countries share borders.]) ]
]

#slide(title:"De Brujin Graphs", outlined:false)[
 #text(.9em)[#align(top)[Using the _Hobbit_ example, I can plot the graph connecting each kmer to every other kmer that has an overlap.]]
 #text(size:.5em)[ #figure(image("images/crpd-graph.pdf", width: auto, height: 80%, fit:"contain"), caption: [A graph of the 5-length kmers from the first sentence of The Hobbit.]) ]
]

#slide(title:"De Brujin Graphs", outlined:false)[
 #text(1em)[#align(top)[This kind of graph is composed of kmers with k-1 overlapping characters.\ AKA a De Brujin graph:]]
 #place(center, dy: 10%, dx:0%)[#framed(back-color: white)[#align(left)[#text(.8em)[$k = 5$\ #text(blue)[inaho]\ ~naho#text(blue)[l]\ ~~~ahol#text(blue)[e]\ ~~~~~hole#text(blue)[i]\ ~~~~~~~olei#text(blue)[n]\ ~~~~~~~~~lein#text(blue)[t]\ ~~~~~~~~~~~eint#text(blue)[h]\ ~~~~~~~~~~~~~~inth#text(blue)[e] ...\ #text(blue)[inaholeintheground...]]]]]
 #align(bottom)[Following each edge along the graph, the original sentence can be constructed using the last letter of each word.]
]


#title-slide[My Approach]


#slide(title: "Start from what you know", outlined: false)[
  Instead of exploring the entire graph, anchor on the query and explore outward in both directions.

  #v(.5em)
  #align(center)[#framed(back-color: white)[#set text(.85em); #align(left)[
    Genome: #rect(fill: rgb("5a0d8722"), inset:3pt, radius:3pt)[inaholeinthe#text(theme_col)[*ground*]therelivedahobbit]

    Query: *ground* $arrow.r$ kmers: gro, rou, oun, und

    #v(.3em)
    *Left* (from "gro"): ...ein $arrow.r$ int $arrow.r$ nth $arrow.r$ the $arrow.r$ heg $arrow.r$ egr $arrow.r$ #text(theme_col)[gro]\
    *Right* (from "und"): #text(theme_col)[und] $arrow.r$ ndt $arrow.r$ dth $arrow.r$ the $arrow.r$ her $arrow.r$ ere...

    #v(.3em)
    Result: ...einthe#text(theme_col)[*ground*]there...
  ]]]
]

#slide(title: "Algorithm outline", outlined: false)[
  - Identify kmers that make up the query (_core cloud_)
  - Explore left from the leftmost query kmer (DFS)
  - Explore right from the rightmost query kmer (DFS)
  - Join the longest left + right contigs around the query
]

#slide(title: "Three hyperparameters", outlined: false)[
  
  #grid(rows: (auto, 1fr, 1fr), gutter: 12pt,
    framed(back-color: white)[
      #text(fill: theme_col)[*k*] $arrow.r$ _kmer size_\
      #text(size:.8em)[
        // coverage: how many reads contain a given kmer
        Too small: same kmer appears everywhere #text(fill:gray)[(high coverage, low specificity)]\
        // specificity: a kmer uniquely identifies where it came from
        Too large: kmers exceed read length #text(fill:gray)[(low coverage, high specificity)] 
      ]\
      _Balance uniqueness vs. frequency_
    ],
    framed(back-color: white)[
      #text(fill: theme_col)[*t*] $arrow.r$  frequency threshold\
      #text(size: .8em)[
        Too low: sequencing errors enter the graph as noise\
        Too high: real but rare kmers are discarded\
      ]
      _Balance signal vs. noise_
    ],
    framed(back-color: white)[
      #text(fill: theme_col)[*max\_visits*] $arrow.r$  cycle limit\
      #text(size: .8em)[
        Prevents infinite loops through repeated sequence\
        Fixed at 2: allows passing through a node twice before stopping\
      ]
      _Handle repeats without endless looping_
    ]
  )
]


#title-slide[Results]


#slide(title: "Validation: three test scenarios", outlined: false)[
  #set text(size: .88em)
  #grid(columns: (auto, 1fr), gutter: 10pt,row-gutter:30pt,
    align(top)[*Test 1*], [ #text(theme_col,weight: "bold")[STRT]ABCDEFGABCHIJKDEFENDSTRTABCDEFGABCHIJKDEFEND \
      - Simple linear sequence with cycle at #text(theme_col,weight: "bold")[DEF]
      - Query at the edge of the sequence
      ],
    
    align(top)[*Test 2*], [inaholeinthegroundtherelivedah#text(theme_col,weight:"bold")[obbitnotanast]ydirtywethole...\
    - Central query
    - Explores cycles caused by repeated words like "hobbit" (need for `max_visits` parameter) ],
    
    align(top)[*Test 3*], [ ATCTGCTGA...
    - Simulated DNA reads (A, T, C, G) 
    - Tests performance with a realistic four-letter alphabet and larger read count
    ],

    align(top)[*Unit Tests*], [
      - Test each function against expected output (integrated into GitHub actions)
    ]
  )
]


#slide(title: "Choosing k", outlined: false)[
  #set text(size: .85em)
  #grid(columns: (1.5fr, 1fr), gutter: 16pt,
    figure(image("../out/assigned/k_count.pdf"), caption: [Unique kmers count vs. k]),
    [
      #v(2em)
      - *Small k (<\~10):* nearly every kmer seen repeatedly, very few unique
      - *Medium k (\~25):* unique count peaks; long enough that most kmers are seen only in one read, short enough to still be fully contained within a read 
      - *Large k (\~>25):* kmers approach read length; count collapses
      #v(1em)
      Chosen value: *k = 19*
    ]
  )
]


#slide(title: "Applied to a real sequence", outlined: false)[
  #set text(size: .9em)
  #let purp = rgb("5b35e784")
  #let query = "GGGATCGGCCATTGAACAAGATGGATTGCACGCAGGTTCTCCGGCCGCTTGGGTGGAGAGGCTATTCGGCTATGACTGGGCACAACAGACAATCGGCTGCTCTGATGCCGCCGTGTTCCGGCTGTCAGCGCAGGGGCGCCCGGTTCTTTTTGTCAAGACCGACCTGTCCGGTGCCCTGAATGAACTGCAGGACGAGGCAGCGCGGCTATCGTGGCTGGCCACGACGGGCGTTCCTTGCGCAGCTGTGCTCGACGTTGTCACTGAAGCGGGAAGGGACTGGCTGCTATTGGGCGAAGTGCCGGGGCAGGATCTCCTGTCATCTCACCTTGCTCCTGCCGAGAAAGTATCCATCATGGCTGATGCAATGCGGCGGCTGCATACGCTTGATCCGGCTACCTGCCCATTCGACCACCAAGCGAAACATCGCATCGAGCGAGCACGTACTCGGATGGAAGCCGGTCTTGTCGATCAGGATGATCTGGACGAAGAGCATCAGGGGCTCGCGCCAGCCGAACTGTTCGCCAGGCTCAAGGCGCGCATGCCCGACGGCGATGATCTCGTCGTGACCCATGGCGATGCCTGCTTGCCGAATATCATGGTGGAAAATGGCCGCTTTTCTGGATTCATCGACTGTGGCCGGCTGGGTGT"
  #let contig = "TTCTCCTCTTCCTCATCTCCGGCCTTTCGACCTGCAGCCAATATGGGATCGGCCATTGAACAAGATGGATTGCACGCAGGTTCTCCGGCCGCTTGGGTGGAGAGGCTATTCGGCTATGACTGGGCACAACAGACAATCGGCTGCTCTGATGCCGCCGTGTTCCGGCTGTCAGCGCAGGGGCGCCCGGTTCTTTTTGTCAAGACCGACCTGTCCGGTGCCCTGAATGAACTGCAGGACGAGGCAGCGCGGCTATCGTGGCTGGCCACGACGGGCGTTCCTTGCGCAGCTGTGCTCGACGTTGTCACTGAAGCGGGAAGGGACTGGCTGCTATTGGGCGAAGTGCCGGGGCAGGATCTCCTGTCATCTCACCTTGCTCCTGCCGAGAAAGTATCCATCATGGCTGATGCAATGCGGCGGCTGCATACGCTTGATCCGGCTACCTGCCCATTCGACCACCAAGCGAAACATCGCATCGAGCGAGCACGTACTCGGATGGAAGCCGGTCTTGTCGATCAGGATGATCTGGACGAAGAGCATCAGGGGCTCGCGCCAGCCGAACTGTTCGCCAGGCTCAAGGCGCGCATGCCCGACGGCGATGATCTCGTCGTGACCCATGGCGATGCCTGCTTGCCGAATATCATGGTGGAAAATGGCCGCTTTTCTGGATTCATCGACTGTGGCCGGCTGGGTGTGGCGGACCGCTATCAGGACATAGCGTTGGCTACCCGTGATATTGCTGAAGAGCTTGGCGGCGAATGGGCTGACCGCTTCCTCGTGCTTTACGGTATCGCCGCTCCCGATTCGCAGCGCATCGCCTTCTATCGCCTTCTTGACGAGTTCTTCTGAGGGGATCCGCTGGGAGTTCAAAGGAGGGGTCCCCTATCGAATTACAGTGACTGCAGTATATTCTGGAGGATTAGCTGCTGCACCCTCAGTTTGGGA"
  #let query-idx = contig.position(query)
  #let query-end = if query-idx != none { query-idx + query.len() } else { -1 }

  #grid(columns: (1fr, 1fr), gutter: 16pt,
    [
      #text(font: "Courier New", size: .8em)[
        #set par(spacing: 1pt, leading: 2pt)
        #let chunk = 40
        #let n = calc.ceil(contig.len() / chunk)
        #for i in range(0, n) {
          let cs = i * chunk
          let ce = calc.min((i + 1) * chunk, contig.len())
          let seg = contig.slice(cs, ce)
          let hl-start = calc.max(query-idx, cs) - cs
          let hl-end = calc.min(query-end, ce) - cs
          if query-idx != none and hl-start < hl-end {
            seg.slice(0, hl-start)
            text(fill: theme_col, weight: "bold", seg.slice(hl-start, hl-end))
            seg.slice(hl-end)
          } else { seg }
          linebreak()
        }
      ]
    ],
    [
      #v(1em)
      *BLASTn result:*\
      _Mus musculus_ Col1a2-G610C allele\
      (type I procollagen alpha2 chain, exon 33)

      #v(.8em)
      *What this means:*\
      Col1a2 encodes a structural protein in bone. The G610C mutation is a well-characterized mouse model of *osteogenesis imperfecta*, aka, brittle bone disease. This sequence likely derives from a transgenic mouse used to study that condition.

      #v(.8em)
      #text(fill: theme_col)[Query sequence shown in purple.]
    ]
  )
]


#title-slide[Conclusions]

#slide(title: "Takeaways", outlined: false)[
  - Anchoring assembly on a known query makes targeted _de novo_ assembly tractable
    - exploration starts at most relavent core
  - Without ground truth, parameter tuning relies on test performance
  - The assembled contig aligns confidently to the _Mus musculus_ Col1a2-G610C transgenic allele which is consistent with a mouse model for osteogenesis imperfecta
]


#slide(title: "Limitations & future directions", outlined: false)[
  *Current limitations:*
  - No explicit error correction: the frequency threshold `t` is a blunt proxy
  - No ground truth so correctness cannot be confirmed

  #v(.5em)
  *Future directions:*
  - Coverage-weighted edges
    - trust high-coverage paths more than low-coverage ones
  - Bubble detection to replace reliance on a fixed `max_visits` parameter 
]


// ─────────────────────────────────────────────
// BIBLIOGRAPHY
// ─────────────────────────────────────────────
#let bib = bibliography("bibliography.bib")
#bibliography-slide(bib, extra: align(bottom)[ https://github.com/canderson318/research-methodology-programming-assignment ])
