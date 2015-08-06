import time
import pickle

def gpsHasStarted():
	try:
		gps = pickle.load(open("gps.p",'rb'))
	except (OSError,IOError,NameError):
		gps = [0,0]

	if gps[0]>1:
		return True
	else:
		return False

end = gpsHasStarted()

while end == False:
	print("Waiting for gps...")
	end = gpsHasStarted()
	time.sleep(1)

print("GPS up and running")

	
