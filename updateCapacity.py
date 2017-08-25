import json  # for formatting the output
import datetime
import time  # for formatting the time from a date
import requests  # for getting the data in the first place
from utils import writeFileWithLog, getLogger
from config import BASE_PATH, URL_WLCG_CAPACITIES, CAPACITY_DATA_LABELS
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Stop it complaining that its not checking certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = getLogger()
logger.debug("Starting")


# define a function which gets the required JSON data for a specific year and
# month
def getData(month, year):
    r = requests.get(URL_WLCG_CAPACITIES.format(year, month), verify=False)
    # example return from this function:
    # {"aaData":[["EGI", "RAL-LCG2", 750, 9012, 90120, 13179200, 24443386]]}
    return r.text


try:
    # this is the path that the JSON will be served from + which ever name from
    # the list of named values below
    path = BASE_PATH + "capacityOverTime"

    # setup the list of data points that we will get from the json data source
    timeData = []
    currentYear = datetime.datetime.now().year
    for year in range(2011, currentYear + 1):
        # If its the final year, only get data for up to and including the
        # current month.
        maxMonth = (13 if year != currentYear
                    else datetime.datetime.now().month + 1)
        for month in range(1, maxMonth):
            d = json.loads(getData(month, year))
            logger.debug("Got a valid JSON response from year: {0}, month: {1}"
                         .format(year, month))
            try:
                toAppend = d["aaData"][0]
                # this is just the way that REBUS returns its data,
                # there is nothing special about the string aaData
            except IndexError:
                logger.warn("Empty JSON data was returned for "
                            "year: {0}, month: {1}".format(year, month))
                # this is necessary because some of the entries in 2012
                # are not in the system for some reason
            else:
                logger.debug("Got data for year: {0}, month: {1}"
                             .format(year, month))
                # make use of the first two values in each list which
                # are: sitename and infrastructure
                # overwrite these with the month and year
                toAppend[0] = year
                toAppend[1] = month
                timeData.append(toAppend)

    # Step through each of the capacity labels: CPU, HESPEC06... etc
    # Keep track of the index which links the label to a column in the returned
    # data.
    for index, name in enumerate(CAPACITY_DATA_LABELS):
        jsonObj = [{"target": name, "datapoints": []}]
        # Step through each datapoint. Create a Grafana-friendly
        # timestamp and append it to a jsonObj which will be served from the
        # 'query' URL.
        for item in timeData:
            dt = datetime.datetime(year=item[0], month=item[1], day=1)
            timestamp = time.mktime(dt.timetuple())
            jsonObj[0]["datapoints"].append([item[index + 2],
                                             int(timestamp) * 1000])
        # Write the query string
        writeFileWithLog(path + name + "/query", json.dumps(jsonObj))
        logger.debug("Written JSON data for {0}".format(name))
except BaseException as ex:
    logger.exception(ex)
