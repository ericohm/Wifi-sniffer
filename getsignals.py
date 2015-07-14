#Eric 2015-07-10
#The kismet program running on linux saves it's log file in an xml format. This script will take this output
#and take out the mac addresses and store the signal strength from each device.

import xml.etree.ElementTree as ET
import pickle
import glob, os
import time
import json


#Nameing the file we save to as default
iteration = "default"

def getGPS():
    '''The drones pixhawk can recieve a command which gives the GPS coordinates for the drone'''
    '''The output from this command is stored in a text file, which means the last row are the most recent coordinates'''
   
    '''Take in the most recent file'''
    files = glob.glob(os.path.abspath("/home/kshan/GPS.txt"))
    files.sort()
    fileX = files[-1]

    '''Read in the last row'''
    with open(fileX, 'rb') as fh:
        last = fh.readlines()[-1].decode()
    last = str(last)

    '''Look for index where the longitude and latitue coordinates begin in this row string'''
    lat_index = last.index("lat")+6
    lon_index = last.index("lon")+6

    '''Since coorinates have 6 decimals, we divide the coordinates by 1000000 and take in the right string for that'''
    '''A coordinate can be either 8 or 9 charachters long'''
    if last[lat_index+9]==",":
        lat = float(last[lat_index:lat_index+8])/1000000
    else:
        lat = float(last[lat_index:lat_index+9])/1000000

    if last[lat_index+9]==",":
        lon = float(last[lon_index:lon_index+8])/1000000
    else:
        lon = float(last[lonindex:lon_index+9])/1000000

    lat = float(lat)
    lon = float(lon)

    return lat,lon
    

def newPoint(x,y):
    '''files variable stores all the netxml files in the folder in a list, it then sorts it and takes out the most recent one'''
    files = glob.glob(os.path.abspath("/home/kshan/Test/*.netxml"))
    files.sort()

    gpsx = x
    gpsy = y
    fileX = files[-1]

    '''Parse the xml and open the last saved dictionary that we save with this script. If no list exists an empty one is created'''
    tree = ET.parse(fileX)
    root = tree.getroot()

    try:
        signals = pickle.load(open(iteration+".p",'rb'))
    except (OSError,IOError):
        signals = []
    
    '''Every signal is linked to a macaddress and takes the time stamp, gps coordinates and signal strength and puts it  '''
    '''in a json compatiable dictionary'''
    for info in root.findall('wireless-network'):
        last_time = info.attrib["first-time"]
        bssid = info.find('BSSID').text
        last_signal = int(info.find('snr-info')[0].text)+10
        essid = info.find('SSID')
        if essid == None:
            temp = {"Signal":last_signal,"Time":last_time, "Longitude":gpsx,"Latitude":gpsy}
            if bssid in signals:
                if signals[bssid][-1]["Time"] != last_time:
                    signals[bssid].append(temp)
            else:
                signals[bssid]=[]
                signals[bssid].append(temp)
        else:
            print("This is a router")

    #for i in signals:
        #print(i,signals[i])
        #print(signals[i][len(signals[i])-1])
    print("\n")
    print(signals)
    #time.sleep(0.1)

    '''Saving the dictionary to a pickle and a text file'''
    pickle.dump(signals,open(iteration+".p","wb"))
    jsonString = json.dumps(signals)
    text_file = open("signals.txt", "w")
    text_file.write(jsonString)
    text_file.close()

x,y = getGPS()
newPoint(x,y)
