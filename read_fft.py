#!/usr/bin/env python
import scipy
import os
from time import *
import time
import pickle

threshold = -40
iteration = "gsm_default"

class countvar:
	count_interval = 0
	signals = {"Entries":[]}

def getGPS():
	cords = pickle.load(open("gps.p","rb"))
	latitude = cords[0]
	longitude = cords[1]
	theTime = cords[2]
	return latitude,longitude,theTime

#def getTime():
#    stamp = pickle.load(open("time.p",'rb'))
#    return stamp

def calculate_gsm(lat,lon,time):
	print("how")
	f = scipy.fromfile(open("gsm_power.txt"), dtype=scipy.int8)
	print("long")
	temp = f[countvar.count_interval:len(f)]
	count1 = 0
	count2 = 0
	person = 0
	last = False
	numberOfPersons = 0
	for j in temp:
		if j > threshold:
			count1 = count1 + j
			count2 = count2+1
			if last == True:
				person = person +1
			else:
				person=1
			last = True
		else:
			person = 0
			last = False

		if person >39:
			numberOfPersons = numberOfPersons +1
			person = 0

	if numberOfPersons>0:
		average = count1/max(count2,1)

		temp = {"Signal":average, "Longitude":lon,"Latitude":lat,"VideoTime":time,"Persons":numberOfPersons}
		print(temp)
		countvar.signals["Entries"].append(temp)
		#print(countvar.signals)


	countvar.count_interval = len(f)

for i in range(0,1000000):
	lat,lon,thetime=getGPS()
	calculate_gsm(lat,lon,thetime)
	'''print(countvar.count_interval)'''
	time.sleep(1)
	pickle.dump(countvar.signals,open(iteration+".p","wb"))

