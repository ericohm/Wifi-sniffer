import math
import xml.etree.ElementTree as ET
import pickle
import glob, os
import time
import json

#Eric Ohman 24/7 2015
#This script takes in all our points for each macAddress and returns our best estimate of where that person is
#based on the signal strengths.
iteration = "default"
try:
	signals = pickle.load(open(iteration+".p",'rb'))
except (OSError,IOError,NameError):
	signals = {}

#Some out commented code, I chose to go with comparing the radius to eachoter instead of absolute distances.
#def getRadius2(x):
#    logdistance = 1+math.log10(2.4*10**6)-187/20+2/5-x/20
#    radius = 10**logdistance
#    return min(radius,200)

#This function returns the radius, longitude and latitude for each signal.
#Wifi signal strength are given in dBM and -xdBM/(-x+1)dbm = 1.12.
#Therefor we give the radius in releation to the highest one in the list.
def getRadius(macAdress):
	radius = []
	sig = signals[macAdress]["Entries"]
	theMax = float(-100)
	for i in sig:
		temp = [float(i["Signal"]),i["Latitude"],i["Longitude"],i["VideoTime"]]
		theMax = float(max(theMax,i["Signal"]))
		radius.append(temp)

	for i in radius:
		i[0] = 1.12**(theMax-i[0])
	return radius

#Simple function that returns our best estimate for a particular macAdress based on the signal strengths and coordinates.
def centerOfMass(macAdress):
    points = getRadius(macAdress)
    points.sort(key =lambda x: x[0])
    points = points[0:min(3,len(points))]
    lon = 0
    lat = 0
    m = float(0.0)
    for i in points:
        temp = float(i[0]**2)
        lat = lat+i[1]/temp
        lon = lon+i[2]/temp
        m = m+1/temp
    longitude = round(lon/m,6)
    latitude = round(lat/m,6)

    timeList = []
    for i in points:
    	dist = math.hypot(longitude - i[2], latitude - i[1])
    	tempor = [dist,i[3]]
    	timeList.append(tempor)

    mindistance = 1000
    theTime = 0
    for i in timeList:
    	if i[0]<mindistance:
    		mindistance = i[0]
    		theTime = i[1]

    return {"Longitude":longitude, "Latitude":latitude,"VideoTime":theTime}

#We add an estimate for every macAdress in signals.
for i in signals:
	signals[i]["Estimate"] = centerOfMass(i)


#Save the signals so we can upload it via the app.js script.
pickle.dump(signals,open(iteration+".p","wb"))
jsonString = json.dumps(signals)
text_file = open("wifi_signals.txt", "w")
text_file.write(jsonString)
text_file.close()
