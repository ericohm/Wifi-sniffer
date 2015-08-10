import math
import xml.etree.ElementTree as ET
import pickle
import glob, os
import time
import json

#Eric Ohman 9/8 2015
#This script converts all the points we have from the gsm signals into json compatiable objects which we can upload to the database.
iteration = "gsm_default"
try:
	signals = pickle.load(open(iteration+".p",'rb'))
except (OSError,IOError,NameError):
	signals = {}

#Save the signals so we can upload it via the app.js script.
pickle.dump(signals,open(iteration+".p","wb"))
jsonString = json.dumps(signals)
text_file = open("gsm_signals.txt", "w")
text_file.write(jsonString)
text_file.close()
