"""
Note that as of 09/08/2017, this script does not work because Ganglia no
longer returns datapoints as JSON.

For example:
http://ganglia.gridpp.rl.ac.uk/ganglia/graph.php?r=hour&c=CASTOR_Repack&m=load_one&s=by+name&mc=2&g=network_report&json=1
"""
from __future__ import print_function
import json  # to parse stuff
from os import makedirs  # to make folders
import requests  # to make url requests
import re  # to find the title in the URL
from utils import writeFileWithLog

print(__doc__)
raise Exception("No longer working...")


# IMPORTANT: the link should have the 'r=...&' removed from the query string
listOfGangliaURLs = [{
    "link": ("http://ganglia.gridpp.rl.ac.uk/ganglia/graph.php?me=RAL+"
             "Tier-1&m=load_one&s=by+name&mc=2&g=network_report&json=1"),
    "title":
    "GridNetwork"
}, {
    "link": ("http://ganglia.gridpp.rl.ac.uk/ganglia/graph.php?me=RAL+"
             "Tier-1&m=load_one&s=by+name&mc=2&g=cpu_report&json=1"),
    "title":
    "GridCPU"
}]

for urlDict in listOfGangliaURLs:
    # raise an error if the r= key hasn't been removed in the links above
    assert len(re.findall(r"(&|^)r=", urlDict["link"].split("?", 2)[1])) == 0

    # initialise the gangliaObj
    gangliaObj = False

    # go through all the possible timeframes from ganglia
    listOfGangliaWindows = [("hour", 3600), ("2hr", 7200), ("4hr", 14400),
                            ("day", 86400), ("week", 604800),
                            ("month", 2629800), ("year", 31557600),
                            ("3year", 94672800), ("10year", 315576000)]

    for window, seconds in listOfGangliaWindows:
        # get the link above with an aditional querystring parameter - the
        # duration that we want
        r = requests.get(urlDict["link"] + "&r=" + window)
        addition = json.loads(r.text)
        if not gangliaObj:
            # if there is nothing to merge to then its easy, just initialise as
            # the data from ganglia
            gangliaObj = addition  # parse the JSON response
            # gangliaObj is a list of objects where each object is a timeseries
        else:
            # Otherwise, it is more difficult, the datastructures need to be
            # mereged together...
            # Ensure that they both contain the same number of time series
            assert len(gangliaObj) == len(addition)
            for current, new in zip(gangliaObj, addition):
                # Step through each time series with a pair of what is already
                # stored (current) and what this request is adding (new)
                # Setup a place to store the earliest time that we already have
                # data stored for. Initialise this with a value that will not
                # be the smallest.
                earliestDataTime = 10**20
                for pair in current["datapoints"]:
                    # Go through all the pairs of [data, time] and establish
                    # the earliest time that we already have stored.
                    if pair[1] < earliestDataTime:
                        earliestDataTime = pair[1]
                # Add all datapoints whose time refers to something before what
                # we already have saved.
                current["datapoints"] += [
                    pair for pair in new["datapoints"]
                    if pair[1] < earliestDataTime
                ]
        # store the current duration for use in the next window
        durationOfPreviousWindow = seconds
    # create an object to populate with [{"target":name, "datapoints":[]}]
    jsonObj = []
    # go through all the returned combined timeseries
    for timeseries in gangliaObj:
        # fix for some odd character in the metric names for some plots
        timeseries["metric_name"] = timeseries["metric_name"].replace(
            r"\g", "")
        # sort the combined datapoints into cronological order
        timeseries["datapoints"].sort(key=lambda pair: pair[1])
        # go through each data point that isn't NaN and convert the pair of
        # [value, timestamp] to miliseconds and add it to the final object
        jsonObj.append({
            "target":
            timeseries["metric_name"],
            "datapoints": [
                [pair[0], pair[1] * 1000]  # change the timestamp to ms
                for pair in filter(
                    lambda x: x[0] != "NaN",  # remove NaN values
                    timeseries["datapoints"])
            ]
        })
        # use the filter to remove anything containing "NaN" as a value

    if "title" in urlDict:  # if a title has been assigned
        title = urlDict["title"]
    else:
        title = re.findall(r"(?<=[\?&]c=)[^&]*", urlDict["link"])
        # otherwise find the title in the query string
        assert len(title) == 1
        # assume that you only find one match for the title
        title = title[0]

    path = "/var/www/html/grafanaJsonDatasources/fromGanglia"

    try:
        # try making a folder to save everything in
        makedirs(path + title)
        print("folder created: " + path + title)
    except OSError:
        print("folder already exists: " + path + title)

writeFileWithLog(path + title + "/query", json.dumps(jsonObj))
writeFileWithLog(path + title + "/search",
                 json.dumps([point["target"] for point in jsonObj]))
