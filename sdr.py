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
	return latitude,longitude

def calculate_gsm(lat,lon):
  f = scipy.fromfile(open("yo.txt),dtype=scipy.int8)
  temp = f[countvar.count_interval:len(f)]
  count1 = 0
  count2=0
  bit = 0
  
  for j in temp:
    if j > threshold:
      count1 = count1+j
      count2 = count2+1
      bit = 1
    if but == 1:
      average = count1(max(count2,1))
      temp = {"Signal":average,"Longitude":lon,"Latitude":lat}
      countvar.signals["Entries"].append(temp)

  countvar.count_interval = len(f)



for i in range(0,1000):
  lat,lon = getGPS()
  time.sleep(1)
  calculate_gsm(lat,lon)
  pickle.dump(countvar.signals,open(iteration+".p","wb"))






