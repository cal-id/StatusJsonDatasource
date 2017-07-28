import json
import datetime
import time
import os

path = "/var/www/html/grafanaJsonDatasources/capacityOverTime"

listOfNamedValues = ["Physical CPU", "Logical CPU", "HEPSPEC06", "Disk", "Tape"]

with open("timeData","r") as file:
	timeData = json.loads(file.read())

for index, name in enumerate(listOfNamedValues):
	try: 
		os.makedirs(path+name)
		print("folder created: "+path+name)
	except OSError:
		print("folder already exists: "+path+name)

	jsonObj = [{"target":name, "datapoints":[]}]

	for item in timeData:
		dt = datetime.datetime(year=item[0], month=item[1], day=1)
		timestamp = time.mktime(dt.timetuple())
		jsonObj[0]["datapoints"].append([item[index+2],int(timestamp)*1000])

	with open(path+name+"/query", "w") as file:
		file.write(json.dumps(jsonObj))
		print("written file: "+path+name+"/query")
	
	with open(path+name+"/search", "w") as file:
		file.write(json.dumps([name]))
		print("written file: "+path+name+"/query")
