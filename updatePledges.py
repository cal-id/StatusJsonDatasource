from __future__ import print_function
import json  # for formatting the output

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


# define a function which gets the required JSON data for a specific year
def getData(year):
    r = requests.get("http://wlcg-rebus.cern.ch/apps/pledges/resources/"
                     "federation/208/{}/json_datatables".format(year),
                     verify=False)
    return r.text


# Example return from this function
'''
{
  "aaData": [
    [
      "CPU (HEP-SPEC06)",
      3140,
      "",
      "2%",
      157000,
      65000,
      "",
      "13%",
      520000,
      32000,
      "",
      "8%",
      400000,
      46800,
      "",
      "32%",
      146000,
      146940,
      "",
      "12%",
      1223000
    ],
    [
      "Disk (Tbytes)",
      420,
      "",
      "2%",
      21000,
      5875,
      "",
      "13%",
      47000,
      2640,
      "",
      "8%",
      33000,
      4050,
      "",
      "27%",
      14900,
      12985,
      "",
      "11%",
      115900
    ],
    [
      "Tape (Tbytes)",
      312,
      "Deployed when needed",
      "2%",
      15600,
      14500,
      "Deployed when needed",
      "13%",
      116000,
      8000,
      "Deployed when needed",
      "8%",
      100000,
      12630,
      "Deployed when needed",
      "49%",
      25800,
      35442,
      "",
      "14%",
      257400
    ]
  ]
}
'''

# this is the path that the JSON will be served from + which ever name from the
# list of named values below
path = "/var/www/html/grafanaJsonDatasources/pledgesOverTime"

# this is the dictionary of different data points that you get can from the
# data
dictionaryOfTimeData = {"CPU": [], "Disk": [], "Tape": []}
# go through the years up to the current year
for year in range(2009, datetime.datetime.now().year + 1):
    d = json.loads(getData(year))
    for toAppend in d["aaData"]:
        key = toAppend[0].split()[0]  # should be one of CPU, Disk or Tape
        # make use of the first value in each list which is name of data
        # overwrite these with the year
        toAppend[0] = year
        dictionaryOfTimeData[key].append(toAppend)

for key in dictionaryOfTimeData:  # Step through CPU, Disk, Tape
    # Create the folders
    try:
        os.makedirs(path + key)
        print("folder created: " + path + key)
    except OSError:
        print("folder already exists: " + path + key)

    try:
        os.makedirs(path + key + "SumOnly")
        print("folder created: " + path + key)
    except OSError:
        print("folder already exists: " + path + key)

    # this is the order that the experiments occur in the data
    # on the old dashboard, SUM is the important metric
    orderOfExperimentsInData = ["ALICE", "ATLAS", "CMS", "LHCb", "SUM"]

    # the list to be populated by instances of {"target":str, "datapoints":[]}
    jsonObj = [{
        "target": experiment,
        "datapoints": []
    } for experiment in orderOfExperimentsInData]

    for dataInAYear in dictionaryOfTimeData[key]:
        # Create a timestamp for this data point
        dt = datetime.datetime(year=dataInAYear[0], month=12, day=31)
        timestamp = time.mktime(dt.timetuple())
        # this is a float so ends with a .0
        # start at index 1, step through in multiples of 4
        for index, item in enumerate(dataInAYear[1::4]):
            # step through the data for each experiment
            jsonObj[index]["datapoints"].append([item, int(timestamp) * 1000])
            # convert timestap to an integer and miliseconds

    with open(path + key + "/query", "w") as fh:
        fh.write(json.dumps(jsonObj))
        print("written file: " + path + key + "/query")

    with open(path + key + "/search", "w") as fh:
        fh.write(json.dumps(orderOfExperimentsInData))
        print("written file: " + path + key + "/search")

    with open(path + key + "SumOnly" + "/query", "w") as fh:
        fh.write(json.dumps([jsonObj[-1]]))
        print("written file: " + path + key + "SumOnly" + "/query")

    with open(path + key + "SumOnly" + "/search", "w") as file:
        file.write(json.dumps([orderOfExperimentsInData[-1]]))
        print("written file: " + path + key + "SumOnly" + "/search")
