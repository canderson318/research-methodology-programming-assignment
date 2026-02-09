/*
ROOT=/Users/canderson/Documents/school/res-meth-class/programming-assignment
RELPATH=deliverables/module-1/presentation                              
cd $ROOT/$RELPATH/images/ && ./process-images.sh || exit 1 
cd $ROOT || exit 1
typst compile --root $ROOT  $RELPATH/main.typ 


typst watch --root $ROOT  $RELPATH/main.typ 



open deliverables/module-1/presentation/main.pdf

*/

#import "lib.typ": *
#import "pseudocode.typ": *

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
  // theme: "dusky", // bluey  reddy  greeny  yelly  purply  dusky  darky
  // theme: rgb("451860"), 
  theme: theme_col, 
  font: "Fira Sans",
  font-size: 20pt,
  link-style: "color",
  show-progress: true,
)

// The front slide is the first slide of your presentation
#front-slide(
  title: "Sequence Assembly Plan",
  subtitle: "Research Methods in Biomedical Informatics",
  authors: "Christian Anderson",
  // info: today.display( "[day] [month repr:long] [year]"),
  info: datetime(year:2026,month:2, day:17).display( "[day] [month repr:long] [year]")
)

// Custom outline
#table-of-contents()

#title-slide[Overview]

#slide( outlined: false)[
  #framed(title: "Problem")["Create a program that takes as input the set of all next-generation sequencing reads identified in a sample and an initial query sequence and returns the largest sequence contig that can be constructed from the reads that contains the initial query sequence."]
]

#slide( outlined: false)[
  
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

#slide( outlined: false)[
  #grid(columns:(2fr,1fr,2fr), gutter: 10pt,
    [#align(center)[#image("images/shredded-newspaper.jpg", height: 200pt, fit:"contain")]],
    [#text(3em,theme_col)[#align(center)[$arrow.r.filled$]]],
    [#align(center)[#image("images/reconstructed-newspaper.jpg", height: 200pt, fit:"contain")]],
    // [#grid.cell(colspan:2,[#framed()[Shred 100 newspapers reconstruct the original document by comparing each strand to every other, taping matches together along the way. Find the article that contains a sentence you are interested in.]])],
  )
]


#let sl(overlay:none)= slide(title:"What are kmers?", outlined: true)[
  
  #set align(top+center); #set text(size: .8em)
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
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Simulate Reads by taking random substrings of different length]])
  #framed(back-color: white)[#align(left)[inahole\ intheground\ edahobbitno\ itnotanastydirty ...]]
  ])

#sl(overlay:[
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Remove non-alphanumeric characters]])
  #framed(back-color: white)[inaholeinthegroundtherelivedahobbitnotanastydirty...]
  #block(inset:(x:0cm,y:0cm),height:0cm, fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Simulate Reads by taking random substrings of different length]])
  #framed(back-color: white)[#align(left)[inahole\ intheground\ edahobbitno\ itnotanastydirty ...]]
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Chop into $k$ length 'mers]])
  #framed(back-color: white)[#align(left)[$k = 5$\ inaho, nahol, nahole, aholei, holein, ... itnot, tnota, notan, otana ...]]
  ])

#sl(overlay:[
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Remove non-alphanumeric characters]])
  #framed(back-color: white)[inaholeinthegroundtherelivedahobbitnotanastydirty...]
  #block(inset:(x:0cm,y:0cm),height:0cm, fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Simulate Reads by taking random substrings of different length]])
  #framed(back-color: white)[#align(left)[inahole\ intheground\ edahobbitno\ itnotanastydirty ...]]
  #block(inset:(x:0cm,y:0cm), height:0cm,fill: white,radius:.2cm,[#set text(.8em,fill: blue);#emph[Chop into $k$ length 'mers]])
  #framed(back-color: white)[#align(left)[$k = 5$\ inaho, nahol, nahole, aholei, holein, ... itnot, tnota, notan, otana ...]]
  #place(bottom+right,dx:2cm, dy:-2cm)[#block(inset:(x:1cm,y:1cm), fill: none,radius:.2cm,[#set text(1.5em,fill: red);#strong[How do we work backwards?] ])]
  ])

  


#slide(title:"What is a graph?", outlined:true)[
 #text(.9em)[#align(top)[A graph is a structure used to encode connections between things.]]
 #text(size:.5em)[ #figure(image("images/simple-graph.png", width: auto, height: 60%, fit:"contain"), caption: [A simple graph used to represent how countries share borders.]) ] //@simple_graph
 #text(.9em)[#align(bottom)[I can use a graph to connect kmers that are similar to each other and reconstruct the original string by following each connection.]]
]


#slide(title:"What is a graph?", outlined:false)[
 #text(.9em)[#align(top)[Using the previous example, I can plot the graph connecting each kmer to every other kmer that has an overlap.]]
 #text(size:.5em)[ #figure(image("images/crpd-graph.pdf", width: auto, height: 80%, fit:"contain"), caption: [A graph of the 5-length kmers from the first sentence of The Hobbit.]) ]
]


#slide(title:"What is a graph?", outlined:false)[
 #text(1em)[#align(top)[This kind of graph is composed of kmers with k-1 overlapping characters.\ AKA a De Brujin graph:]]
 #place(center, dy: 10%, dx:0%)[#framed(back-color: white)[#align(left)[#text(.8em)[$k = 5$\ #text(blue)[inaho]\ ~naho#text(blue)[l]\ ~~~ahol#text(blue)[e]\ ~~~~~hole#text(blue)[i]\ ~~~~~~~olei#text(blue)[n]\ ~~~~~~~~~lein#text(blue)[t]\ ~~~~~~~~~~~eint#text(blue)[h]\ ~~~~~~~~~~~~~~inth#text(blue)[e] ...\ #text(blue)[inaholeintheground...]]]]]
 #align(bottom)[Following each edge along the graph, the original sentence can be constructed using the last letter of each word.]
]



// #title-slide[Technical Approach]
#title-slide[Development Plan]

#slide()[
  #align(center)[#image("images/dev-flowchart.svg")]
]


#slide(title:"Process reads", outlined:true)[
  #set text(size:.8em)
  - Make k-length strings (kmers) from reads.
  - Record kmer frequencies.
  - Filter out infrequent kmers below some threshold $tau$.
  - Filter for unique kmers.
  - Return list of unique kmers $S$.
  #pad(left: 1.5em,top:-.1em)[
    #text(size:.8em)[
      #pc_process
    ] 
  ]

]


#slide(title:"Compare Kmers", outlined:true)[
  
  #set text(size:.8em)
  - Test how each kmer aligns with every other.
  - Return an adjacency matrix where a value of _1_ means the kmer at the row index matches the string of the column index.
  #pad(left: 1.5em)[
    #text(size:.8em)[
      #pc_compare
    ]
  ]
]


#slide(title: "Create Contiguous Sequences", outlined:true)[
  #set text(size: .8em)
  #grid(columns: (1fr, 1fr),rows: (auto, 3fr,auto),gutter: .2em,

    [#grid.cell(colspan: 2)[
      - Concatenate every possible combination of adjacent strings.
      - Return a list of contiguous sequences _contigs_
      #pad(left: 1.5em, bottom: 1em)[#emph[for every string find the next closest strings and for each of these append it to the end of the previous]]
    ]],

    [#align(center + top)[#figure(image("images/crpd-graph.pdf", height: 77%, fit: "contain"),caption: [A graph of the 5-length kmers from the first sentence of _The Hobbit_.])]],

    [#align(center + top)[#figure(image("images/crpd-line-graph.pdf", height: 77%, fit: "contain"),caption: [A graph of the 9-length kmers from the first sentence of _The Hobbit_.])]],

    [#grid.cell(colspan:2)[#align(center+bottom)[#text(blue)[5-letter versus 9-letter kmers]]]]
  )
]


#slide(title:"Create Contiguous Sequences", outlined:true)[
  #grid(columns:(1.3fr , 1fr),rows:(300pt), gutter:.2em, 
    [
      #set align(left); #set text(size:.5em)
        // #figure(
        #image("images/stones.jpg", height: 200pt)
        // , caption:[Stones scattered in a river.])//@river_stones
    ],
    [
      #set align(right); #set text(size:.5em)
      // #figure(
      #pad(right:5em)[
        #image("images/single-path-stones.jpg", height: 200pt)
      // , caption:[Stones in a river arranged in a line.])//@river_footpath
      ]
    ])
]


#slide(title: "Create Contiguous Sequences, cont.")[
  #set align(top+left)
  #set text(size:.55em,)
  #place(dx:-8%,dy:0%)[
    #box(width:110%, height:100%)[
      #pc_create_contigs
      ]
  ]
]


#slide(title:"Query Contigs", outlined:true)[
  #set text(size:.8em)
  - Find the longest sequence contig that contains a query sequence.
  #pad(left: 1.5em)[
    #text(size:.8em)[
      #pc_query
    ]
  ]
]


#let highlight(txt, query, color: blue) = {
  let parts = txt.split(query)

  if parts.len() == 1 {
    txt
  } else {
    let out = ()
    for i in range(parts.len()) {
      out.push(parts.at(i))
      if i < parts.len() - 1 {
        out.push(text(fill: color)[#query])
      }
    }
    out.join()
  }
}

#slide(title:"Example Results", outlined:true)[
  #let q= "dirtywetholefilledwiththeendsofwormsandanoozysmell"
  #set align(top)
  *Query:* #text(blue)[#q]\ \
  *Longest contigs with query sequence:*
  
  #let contigs = (
    "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresand",
    "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyhole",
    "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyhole",
    "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewith",
    "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewithnothinginittositdownonortoeatitwasahob",
    "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholeandth",
    "inaholeinthegroundtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholeandthatmeanscomfort",
    "inaholewithnothinginittositdownonortoeatitwasahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresand",
    "inaholewithnothinginittositdownonortoeatitwasahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholeinthegroundtherelivedahob",
    "inaholewithnothinginittositdownonortoeatitwasahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholeinthegroundthatmeanscomfort",
    "inaholewithnothinginittositdownonortoeatitwasahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyhole",
    "inaholewithnothinginittositdownonortoeatitwasahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyhole",
    "inaholewithnothinginittositdownonortoeatitwasahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholeandtherelivedahob",
    "inaholewithnothinginittositdownonortoeatitwasahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholeandthatmeanscomfort",
    "inaholeandtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresand",
    "inaholeandtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholeinthegroundth",
    "inaholeandtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholeinthegroundthatmeanscomfort",
    "inaholeandtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyhole",
    "inaholeandtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewith",
    "inaholeandtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyholewithnothinginittositdownonortoeatitwasahob",
    "inaholeandtherelivedahobbitnotanastydirtywetholefilledwiththeendsofwormsandanoozysmellnoryetadrybaresandyhole"
  )

  #pad(left:1em)[#text(.45em)[
    #for c in contigs {
      highlight(c, q)
      linebreak()
    }
  ]

]]

// #title-slide[Testing]

#slide(title:"Testing", outlined:true)[
  #set align(horizon+center)
  #image("images/test-flowchart.svg", width: 110%)
]



// // // // // // // 
// // // // // // // 
// // // // // // // 
#let bib = bibliography("bibliography.bib")
#bibliography-slide(bib, extra: align(bottom)[ https://github.com/canderson318/research-methodology-programming-assignment ])


