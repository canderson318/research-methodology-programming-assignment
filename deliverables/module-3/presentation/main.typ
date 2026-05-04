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

// The front slide is the first slide of your presentation
#front-slide(
  title: "Sequence Assembly Plan",
  subtitle: "Research Methods in Biomedical Informatics",
  authors: "Christian Anderson",
  info: today.display( "[day] [month repr:long] [year]"),
)

// Custom outline
#table-of-contents()

#title-slide[Overview]


#slide( outlined: false)[
  #framed(title: "Problem")["Create a program that takes as input the set of all next-generation sequencing reads identified in a sample and an initial query sequence and returns the largest sequence contig that can be constructed from the reads that contains the initial query sequence."]
]

#slide(title:"Biological Relevance", outlined: false)[
  #lorem(100)
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
#title-slide[Algorithm Outline]

#slide(title:"", outlined:false)[
  - build graph from left and right of query kmer core graph
  - create left/right contig along the way 
  - construct full contig by selecting longest right + longest left contigs with query in the middle
  - 

]

// // // // // // // 
// // // // // // // 
// // // // // // // 
#let bib = bibliography("bibliography.bib")
#bibliography-slide(bib, extra: align(bottom)[ https://github.com/canderson318/research-methodology-programming-assignment ])


