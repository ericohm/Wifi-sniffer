import glob, os
import base64
files = glob.glob(os.path.abspath("/home/drone1/Wifi/*.jpg"))
files.sort()
picDictionary = {}
for i in files:
	wifi_index = i.index("Wifi")+5
	jpg_index = i.index(".jpg")
	baseString = base64.encodestring(open(i,"rb").read())
	name = i[wifi_index:jpg_index]
	picDictionary[name] = baseString

