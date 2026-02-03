import numpy as np
def alignment(s1,s2):
    """
    Align x to y where x may have matching characters in first window or last window of y
    return how many characters in x from start to window, or from end to end-(window+1)
    and the direction of alignment from x to y 
    - 1 if x aligns to y in the forward direction 
    - -1 if x aligns to y in the reverse direction 
    - 0 if both
    e.g. 
    x: AATTCGGT
    y:    TCGGTCCG
    -> 1
    x:   TTCGGTACTT
    y: AATTCGGT  
    -> -1 
    x:    AAATTTAAATTT
    y: TTTAAATTTAAATTT  
    and 
    x: AAATTTAAATTT
    y:    TTTAAATTTAAATTT  
            -> 0
    :param s1: reference sequence
    :param s2: sequence compare to reference
    """
    align = lambda x,y: sum([_x==_y for _x,_y in zip(x,y)])
    
    steps = np.array(range(0,min(len(s1), len(s2))))
    
    s1res = []
    for step in steps:
        s1res.append(align(s1[step:], s2))

    s2res = []
    for step in steps:
        s2res.append(align(s2[step:], s1))

    s1res = np.array(s1res)
    s2res = np.array(s2res)

    grade = lambda x: (max(x), np.argmax(x))
    
    shift = 0
    direction = 0
    score = 0
    
    if max(s1res) > max(s2res):
        score, shift  = grade(s1res)
        direction = 1
    elif max(s2res) > max(s1res):
        score, shift  = grade(s2res)
        direction = - 1
    else:
        direction = 0

    return score, shift, direction

# import os 
# os.getcwd()
# os.chdir("src")
# from alignment import *
# alignment("AAATTT", "TTTCCGC")

