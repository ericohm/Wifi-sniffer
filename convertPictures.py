import glob, os
import base64
import json

files = glob.glob(os.path.abspath("/home/pi/*.jpg"))
files.sort()
drone = {"Entries":[]}
for i in files:
    	wifi_index = i.index("CORDS: ")+7
    	comma_index = i.index(",")
    	date_index = i.index("DATE")
    	jpg_index = i.index(".jpg")
    	latitude = i[wifi_index:comma_index]
    	longitude = i[comma_index+1:date_index]
	baseString = base64.encodestring(open(i,"rb").read())
	temp = {"Latitude":latitude,"Longitude":longitude,"Image":str(baseString)}
	drone["Entries"].append(temp)

jsonString = json.dumps(drone)
text_file = open("dronepath.txt","w")
text_file.write(jsonString)
text_file.close()
