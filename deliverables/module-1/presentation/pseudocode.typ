
#let pc_process = {
``` 
        let R be a list of strings composed of A, T, C, or G
        let k be an integer 
        let tau be an integer
        let results be an empty list
        let counter be a dictionary 

        # trim each string to length k; keep track of string frequencies
        for r in R:
          l = len(r)
          for i in range(0, l-k+1):
            r_sub = r[i:i+k]
            results += r_sub
            counter[r_sub] += 1

        # save only unique and frequent strings 
        filtered = counter.keys()[counter.values() > tau]

        return filtered
```}

#let pc_compare= {
 ```
        let S be a list of k-length strings
        let m be a square matrix of zeros with dimensions len(S)

        for i in range(len(S)):
          for j in range(len(S)):
            if i does not equal j:
              si = S[i]
              sj = S[j]
              let si_sub be the substring of si from the second character to the last (2 to k)
              let sj_sub be the substring of sj from the first character to the second last (1 to k-1)
              if si_sub equals sj_sub:
                m[i,j] = 1
                else:
                  m[i,j] = 0

        return m
```
}

#let pc_create_contigs= {
```
        let S be as list of k-length strings
        let A be an adjacency matrix between strings in S, with row and column names S, where rows encode outgoing and columns incoming edges

        let colsums be the column sums of A
        let starts be a list of strings of S where colsums equals the minimum value in colsums (S[colsums == min(colsums)])

        contigs = []

        define _recurse as a function of curr, contig, visited:
          row = A[ S==curr, : ] # ``
          nexts = S[row>0] # ``

          if len(nexts):
            contigs+=contig
            stop function execution

          for next in nexts:
            if next in visited:
              contigs+=contig
              continue to next loop
            new_visited = visited.copy() # ensure each branch only sees within branch visits
            new_visited[next] +=1

            _recurse(next, contig+=next[-1], new_visited) # recursivley run function, each time appending contig with the last character of next

          for start in starts:
            let counter be a dictionary 
            counter[start] = 1
            _recurse(start, start, counter)

        return contigs
```
}

#let pc_query = {
```
      let C be the list of contiguous strings
      let q be the query string

      max_l = 0

      for c in C:
        l = len(c)
        if q is in c & l > max_l:
          max_l = l
          longest_with_query = c

      return longest_with_query
```
}
