from __future__ import print_function
import json  # for formatting the output
# for fomatting the output

import datetime
import time
# for formatting the time from a date

import os
# for making the required folders

import requests
# for getting the data in the first place

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# stop it complaining that its not checking certificates


# define a function which gets the required JSON data for a specific year and
# month
def getData(month, year):
    r = requests.get(
        "https://wlcg-rebus.cern.ch/apps/capacities/federation_sites/208/"
        "{}/{}/json_datatables".format(year, month), verify=False)
    # example return from this function:
    # {"aaData":[["EGI", "RAL-LCG2", 750, 9012, 90120, 13179200, 24443386]]}
    return r.text


# this is the path that the JSON will be served from + which ever name from the
# list of named values below
path = "/var/www/html/grafanaJsonDatasources/capacityOverTime"

# this is the list of different data points that you get can from the data
listOfNamedValues = [
    "Physical CPU", "Logical CPU", "HEPSPEC06", "Disk", "Tape"
]

# setup the list of data points that we will get from the json data source
timeData = []
currentYear = datetime.datetime.now().year
for year in range(2011, currentYear + 1):
    # If its the final year, only get data for up to and including the current
    # month.
    maxMonth = (13 if year != currentYear
                else datetime.datetime.now().month + 1)
    for month in range(1, maxMonth):
        d = json.loads(getData(month, year))
        try:
            toAppend = d["aaData"][0]
            # this is just the way that REBUS returns its data,
            # there is nothing special about the string aaData
        except IndexError:
            print("indexError while getting this data: ", year, month)
            # this is necessary because some of the entries in 2012
            # are not in the system for some reason
        else:
            # make use of the first two values in each list which
            # are: sitename and infrastructure
            # overwrite these with the month and year
            toAppend[0] = year
            toAppend[1] = month
            timeData.append(toAppend)

for index, name in enumerate(listOfNamedValues):
    try:
        os.makedirs(path + name)
        print("folder created: " + path + name)
    except OSError:
        print("folder already exists: " + path + name)

    jsonObj = [{"target": name, "datapoints": []}]

    for item in timeData:
        dt = datetime.datetime(year=item[0], month=item[1], day=1)
        timestamp = time.mktime(dt.timetuple())
        jsonObj[0]["datapoints"].append(
            [item[index + 2], int(timestamp) * 1000])

    with open(path + name + "/query", "w") as file:
        file.write(json.dumps(jsonObj))
        print("written file: " + path + name + "/query")

    with open(path + name + "/search", "w") as file:
        file.write(json.dumps([name]))
        print("written file: " + path + name + "/search")
