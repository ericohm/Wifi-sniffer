import scipy
import time

c_index = 0

for i in range(0,1000):
  f=scipy,fromfile(open("yo.txt"),dtype=scipy.float32)
  temp = f[c_index:len(f)]
  
  time.sleep(1)
