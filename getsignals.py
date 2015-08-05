#Eric 2015-07-10
#The kismet program running on linux saves it's log file in an xml format. This script will take this output
#and take out the mac addresses and store the signal strength from each device.

import xml.etree.ElementTree as ET
import pickle
import glob, os
import time
import json
import picamera
import datetime


#Nameing the file we save to as default
iteration = "default"

def getGPS():
	cords = pickle.load(open("gps.p","rb"))
	latitude = cords[0]
	longitude = cords[1]
	return latitude,longitude

def newPoint(lat,lon):
    '''files variable stores all the netxml files in the folder in a list, it then sorts it and takes out the most recent one'''
    files = glob.glob(os.path.abspath("/home/pi/Test/*.netxml"))
    files.sort()
    fileX = files[-1]

    '''Parse the xml and open the last saved dictionary that we save with this script. If no list exists an empty one is created'''
    tree = ET.parse(fileX)
    root = tree.getroot()

    try:
        signals = pickle.load(open(iteration+".p",'rb'))
    except (OSError,IOError):
        signals = {}
        
    '''Every signal is linked to a macaddress and takes the time stamp, gps coordinates and signal strength and puts it  '''
    '''in a json compatiable dictionary'''
    for info in root.findall('wireless-network'):
        last_time = info.attrib["last-time"]
        bssid = info.find('BSSID').text
        last_signal = int(info.find('snr-info')[0].text)
        essid = info.find('SSID')
        if essid == None:
            temp = {"Signal":last_signal,"Time":last_time, "Longitude":lon,"Latitude":lat}
            if bssid in signals:
                if signals[bssid]["Entries"][-1]["Time"] != last_time:
                    signals[bssid]["Entries"].append(temp)
                    print(temp["Signal":])
            else:
            	signals[bssid] = {"Entries":[]}
            	signals[bssid]["Entries"].append(temp)
    for i in signals:
    	print(i)
    	print(signals[i]["Entries"])
    	
    '''Saving the dictionary to a pickle'''
    pickle.dump(signals,open(iteration+".p","wb"))
    
    '''After this script is run for the last time, the script approximate.py is run to add our best estimates'''

def takePicture(lat,lon):
    '''Function that takes in x,y (latitude longitude) and a name and takes a picture, and saves the picture to that name.'''
    ts = time.time()
    st = "DATE: "+datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    with picamera.PiCamera() as camera:
        name = "CORDS: "+str(lat) +","+ str(lon)+st+".jpg"
        camera.capture(name)

lat,lon = getGPS()
newPoint(lat,lon)
takePicture(lat,lon)
