import numpy as np
import time

tt=time.time()
lis = []
for i in range(1000000):
    lis.append(i)
arr = np.array(lis)
tr=time.time() - tt
print(tr)

tt=time.time()
arr = np.array(np.arange(1000000))
tr=time.time() - tt
print(tr)


tt=time.time()
np.subtract(arr, 1)
tr=time.time() - tt
print("np sub: ",tr)

tt=time.time()
for i in range(1000000):
    lis[i] -= 1
tr=time.time() - tt
print("list sub: ",tr)

tt=time.time()
lis=[]
for i in range(10000000):
    lis.append(1)
tr=time.time() - tt
print(tr)

##tt=time.time()
##for i in range(10000000):
##    np.append(arr, 1)
##tr=time.time() - tt
##print(tr)
