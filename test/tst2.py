import time

lis = []
for i in range(1000000):
    lis.append(i)

tt=time.time()
for i in range(1000000):
    lis[i] -= 1
    a = i
tr=time.time() - tt
print(tr)

import numpy as np
 
#standard iterating over np arrays like normal lists is a waste, gives no benefit, actually slows things down.

tt=time.time()
arr = np.array(lis)
for i in range(1000000):
    a = arr[i]
tr=time.time() - tt
print(tr)
