from __future__ import print_function
import json  # for formatting the output
import datetime
import time  # for formatting the time from a date
from utils import writeFileWithLog, makeDirectoryWithLog
from config import (BASE_PATH, URL_WLCG_PLEDGES, PLEDGES_ROW_DATA_LABELS,
                    PLEDGES_EXPERIMENT_DATA_LABELS)
import requests  # for getting the data in the first place
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# stop it complaining that its not checking certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# define a function which gets the required JSON data for a specific year
def getData(year):
    r = requests.get(URL_WLCG_PLEDGES.format(year), verify=False)
    return r.text


# Example return from this function
# {
#   "aaData": [
#     ["CPU (HEP-SPEC06)",
#      3140, "", "2%", 157000,
#      65000, "", "13%", 520000,
#      32000, "", "8%", 400000,
#      46800, "", "32%", 146000,
#      146940, "", "12%", 1223000],
#     ["Disk (Tbytes)",
#      420, "", "2%", 21000,
#      5875, "", "13%", 47000,
#      2640, "", "8%", 33000,
#      4050, "", "27%", 14900,
#      12985, "", "11%", 115900],
#     ["Tape (Tbytes)",
#      312, "Deployed when needed", "2%", 15600,
#      14500, "Deployed when needed", "13%", 116000,
#      8000, "Deployed when needed", "8%", 100000,
#      12630, "Deployed when needed", "49%", 25800,
#      35442, "", "14%", 257400]
#   ]
# }

# this is the path that the JSON will be served from + which ever name from the
# list of named values below
path = BASE_PATH + "pledgesOverTime"

# This is the dictionary containing a list of the rows returned in the JSON
# for each year. The following for loops populates it.
dictionaryOfTimeData = dict((key, []) for key in PLEDGES_ROW_DATA_LABELS)
for year in range(2009, datetime.datetime.now().year + 1):
    d = json.loads(getData(year))
    # Step through each row in the table of data. See above for example.
    for toAppend in d["aaData"]:
        # Get the first word of the first entry in this row to use as a key
        # in dictionaryOfTimeData. Store the year in it's place as the first
        # entry.
        key = toAppend[0].split()[0]  # should be one of CPU, Disk or Tape
        toAppend[0] = year
        dictionaryOfTimeData[key].append(toAppend)

for key in dictionaryOfTimeData:  # Step through CPU, Disk, Tape
    # For each of CPU, Disk, Tape (`key`): dictionaryOfTimeData[key]
    # stores a list of each years worth of column entries (see above).
    # Each column entries list starts with the year (replacing the key) and is
    # followed by five sets of four values.

    # The four values appear to be something like:
    #    [pledgeValue, comment, % of total, total].
    # We are interested in pledgeValue so we start at index 1 and step through
    # in multiples of 4.

    # Each of the five sets refer to accounting for a different experiment (or
    # the sum over all four). The labels for these sets are defined in the
    # config variable `PLEDGES_COL_DATA_LABELS`.

    # This object is to be populated by the following for loop. It should end
    # up as a list of five objects - one for each experiment and the sum.
    # Each object contains:
    #  - 'target' - a description of the data (experimentName)
    #  - 'datapoints' - a list of data, timestamp pairs for a grafana time plot
    jsonObj = [{"target": experimentName, "datapoints": []}
               for experimentName in PLEDGES_EXPERIMENT_DATA_LABELS]
    # Step through each year
    for dataInAYear in dictionaryOfTimeData[key]:
        # Create a timestamp for these data points
        dt = datetime.datetime(year=dataInAYear[0], month=12, day=31)
        timestamp = int(time.mktime(dt.timetuple())) * 1000  # Convert to ms
        # Start at index 1, step through in multiples of 4 to step through the
        # data for each experiment in this year.
        for index, item in enumerate(dataInAYear[1::4]):
            jsonObj[index]["datapoints"].append([item, timestamp])

    writeFileWithLog(path + key + "/query", json.dumps(jsonObj))
    writeFileWithLog(path + key + "SumOnly" + "/query",
                     json.dumps([jsonObj[-1]]))
