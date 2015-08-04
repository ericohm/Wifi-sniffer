#Eric 2015-07-10
#The kismet program running on linux saves it's log file in an xml format. This script will take this output
#and take out the mac addresses and store the signal strength from each device.

import xml.etree.ElementTree as ET
import pickle
import glob, os
import time
import json
import picamera


#Nameing the file we save to as default
iteration = "default"

def getGPS2():
    '''The drones pixhawk can recieve a command which gives the GPS coordinates for the drone'''
    '''The output from this command is stored in a text file, which means the last row are the most recent coordinates'''
   
    '''Take in the most recent file'''
    files = glob.glob(os.path.abspath("/home/pi/test.txt"))
    files.sort()
    fileX = files[-1]

    '''Read in the last row'''
    with open(fileX, 'rb') as fh:
        last = fh.readlines()[-1].decode()
    last = str(last)

    '''Look for index where the longitude and latitue coordinates begin in this row string'''
    lat_index = last.index("lat")+6
    lon_index = last.index("lon")+6

    lat_comma = last[lat_index:lat_index+12].index(",")
    lat_string = last[lat_index:lat_index+lat_comma]
    lat = float(lat_string)/(10**7)

    lon_comma = last[lon_index:lon_index+12].index(",")
    lon_string = last[lon_index:lon_index+lon_comma]
    lon = float(lon_string)/(10**7)

    return lat,lon

def getGPS():
	realcords = False
	while realcords ==False:
		cords = pickle.load(open("gps.p","rb"))
		latitude = cords[0]
		longitude = cords[1]
		if latitude != None:
			realcords = True
		time.sleep(1)
		print(latitude,longitude)
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
            else:
            	signals[bssid] = {}
            	signals[bssid]["Entries"] = []
            	signals[bssid]["Entries"].append(temp)

    '''Saving the dictionary to a pickle'''
    pickle.dump(signals,open(iteration+".p","wb"))
    
    '''After this script is run for the last time, the script approximate.py is run to add our best estimates'''

def takePicture(lat,lon):
    '''Function that takes in x,y (latitude longitude) and a name and takes a picture, and saves the picture to that name.'''
    with picamera.PiCamera() as camera:
        name = str(lat) +","+ str(lon)+".jpg"
        camera.capture(name)

lat,lon = getGPS()
newPoint(lat,lon)
takePicture(lat,lon)
