#Eric 2015-07-10
#The kismet program running on linux saves it's log file in an xml format. This script will take this output
#and take out the mac addresses and store the signal strength from each device.

#Big edit on august 6th, we decided to try this out on the computer. All code which involves rasperry pi specific modules
#and code, i.e. the picamera is commented out. 
import xml.etree.ElementTree as ET
import pickle
import glob, os
import time
import json
#import picamera
import datetime


#Nameing the file we save to as default
iteration = "default"

#Another threed is run where we contionously save the coordinates to a file called gps.p
#The script which saves the coordinates is called gpstotext.py
def getGPS():
    cords = pickle.load(open("gps.p","rb"))
    latitude = cords[0]
    longitude = cords[1]
    theTime = cords[2]
    return latitude,longitude,theTime


#This is where we save the information from the wifi togheter with gps coordinates.
def newPoint(lat,lon,video_time):
    '''files variable stores all the netxml files in the folder in a list, it then sorts it and takes out the most recent one'''
    files = glob.glob(os.path.abspath("/home/ericsson/*.netxml"))
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
            temp = {"Signal":last_signal,"Time":last_time, "Longitude":lon,"Latitude":lat,"VideoTime":video_time}
            if bssid in signals:
                if signals[bssid]["Entries"][-1]["Time"] != last_time:
                    signals[bssid]["Entries"].append(temp)
            else:
            	signals[bssid] = {"Entries":[]}
            	signals[bssid]["Entries"].append(temp)
    print(signals)
#    for i in signals:
#    	print(i)
#    	print(signals[i]["Entries"])
    	
    '''Saving the dictionary to a pickle'''
    pickle.dump(signals,open(iteration+".p","wb"))
    
    '''After this script is run for the last time, the script approximate.py is run to add our best estimates'''


#We have a program that runs in the background, keepig track of how long the video has recorded
#def getTime():
#    stamp = pickle.load(open("time.p",'rb'))
#    return stamp


#Commented out everything because raspberry
#def takePicture(lat,lon):
#    '''Function that takes in x,y (latitude longitude) and a name and takes a picture, and saves the picture to that name.'''
#    ts = time.time()
#    st = "DATE: "+datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#    with picamera.PiCamera() as camera:
#        name = "CORDS: "+str(lat) +","+ str(lon)+st+".jpg"
#        camera.capture(name)

lat,lon,time = getGPS()
newPoint(lat,lon,time)
#takePicture(lat,lon)
