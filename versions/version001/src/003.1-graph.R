
pacman::p_load(dplyr, ggplot2, igraph, magrittr)
rm(list = ls()); gc()

'out/003' %>% 
    {if(!dir.exists(.)) dir.create(.)}

mat <- read.table("out/002/alignment-res.csv",sep = ",",header = TRUE)

mat = mat[,-1]
rownames(mat) <- colnames(mat)
mat = data.matrix(mat)

for(i in 1:nrow(mat)){
    mat[i, mat[i, ] != max(mat[i,])] <- 0
}

g = graph_from_adjacency_matrix(mat, weighted =  TRUE, diag = FALSE, mode = 'directed')

# start = V(g)[degree(g, mode = 'in') ==0][1]
start = 'AAATTTCCCGGG'

walk <- random_walk(
  g,
  start = start,
  steps = vcount(g) - 1,
  mode = "out",
  weights = E(g)$weight
)

path <- V(g)[walk]$name
cat(path, sep = "\n")

set.seed(1203)
h=w=20
pdf('out/003/graph.pdf', height = h, width = w)
plot.igraph(g)
dev.off()
## TRUTH
# AAATTTCCCGGG
# → TTTCCCGGGCGCG
# → CCCGGGCGCGATCGT
# → GGCGCGATCGTATCCGTA
# → GCGATCGTATCCGTATC