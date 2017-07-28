import json
import datetime
import time
import os

path = "/var/www/html/grafanaJsonDatasources/capacityOverTime/"

try: 
	os.makedirs(path)
	print("folder created")
except OSError:
	print("folder already exists")

with open("timeData","r") as file:
	timeData = json.loads(file.read())


listOfNamedValues = ["Physical CPU", "Logical CPU", "HEPSPEC06", "Disk (GB)", "Tape (GB)"]
jsonObj = []

for name in listOfNamedValues:
	jsonObj.append({
		"target":name,
		"datapoints":[]
	})

for item in timeData:
	dt = datetime.datetime(year=item[0], month=item[1], day=1)
	timestamp = time.mktime(dt.timetuple())
	for index, point in enumerate(item[2:]):
		jsonObj[index]["datapoints"].append([point,int(timestamp)*1000])

with open(path+"query", "w") as file:
	file.write(json.dumps(jsonObj))
