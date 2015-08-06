import pickle
import glob, os
import json


try:
	signals = pickle.load(open("gsm_default.p",'rb'))
except (OSError,IOError,NameError):
	signals = {}

jsonString = json.dumps(signals)
text_file = open("gsm_signals.txt", "w")
text_file.write(jsonString)
text_file.close()
