import json
# import json so that we can format output

path = "/var/www/html/"
additionalPathToNoticeboard = "status/grid/noticeboard.txt"
additionalPathToJsonSource = "grafanaJsonDatasources/notices/query"

jsonObj = [{"columns":[],"rows":[],"type":"table"}]
# the object which will eventually be converted into JSON

jsonObj[0]["columns"]=[
	# preset the titles of the columns of the table
	{"text": "Date"},
	{"text": "Added by"},
	{"text": "Subject"},
	{"text": "Description"}
]

with open(path + additionalPathToNoticeboard, "r") as file:
	for line in file: # step through each line in the file
		if line != "\n":
			cols = line.split(";") # split each line into cols
			'''
			for example a cols would look like this:
			[
				'1252589462',
				'Tiju Idiculla',
				'/C=UK/O=eScience/OU=CLRC/L=RAL/CN=tiju idiculla',
				'Castor Database problems',
				'There are some problems on the CMS and GEN instances of the Castor database. The problem is under investigation.\n'
			]
			'''

			jsonObj[0]["rows"].append([
				int(cols[0])*1000, # parse the timestamp into an integer and change into miliseconds
				cols[1], # ignore the certificate
				cols[3],
				cols[4]
			])

try:
	with open(path + additionalPathToJsonSource, "w") as file:
		file.write(json.dumps(jsonObj))
except IOError:
	print("This folder doesn't exist try running setupFolders.py in this directory")
else:
	print("Written to JSON file")
