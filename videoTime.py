import time
import pickle


#This is for keeping track of the video time.
start_time = time.time()
for i in range(0,10):
	stamp = int(round(time.time()-start_time,0))
	pickle.dump(stamp,open("time.p","wb"))
	time.sleep(1)

