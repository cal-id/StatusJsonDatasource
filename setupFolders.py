"""
This script sets up the folders for some of the datasources:
- Disk Servers In Intervention
- Downtimes
- GGUS Tickets
- Notices
- Storage Usage (this has an overall datasource AND one per VO)

For each data source, it creates a top directory:
    BASE_PATH + "something_to_identify_the_datasource"

And a search file within this top directory. This file is downloaded by
Grafana to give it the titles of the data in this URL.

Works with python2 or python3
"""

import os
from utils import writeFileWithLog, makeDirectoryWithLog, getLogger
from config import (BASE_PATH, CAPACITY_DATA_LABELS, PLEDGES_ROW_DATA_LABELS,
                    PLEDGES_EXPERIMENT_DATA_LABELS)
import json

logger = getLogger()
logger.debug("Starting")


def writeSearchFile(path, content):
    """Writes content (string) to a new file 'search' located under path.
    eg /var/www/html/grafanaJsonDatasources/diskServersInIntervention
    writes content to
    /var/www/html/grafanaJsonDatasources/diskServersInIntervention/search
    """
    filePath = os.path.join(path, "search")
    writeFileWithLog(filePath, content)


try:
    # DISK SERVERS IN INTERVENTION
    makeDirectoryWithLog(BASE_PATH + "diskServersInIntervention")
    makeDirectoryWithLog(BASE_PATH + "diskServersInInterventionHTML")
    writeSearchFile(BASE_PATH + "diskServersInIntervention",
                    '["Disk Servers in Intervention"]')
    writeSearchFile(BASE_PATH + "diskServersInInterventionHTML",
                    '["Disk Servers in Intervention HTML"]')

    # DOWNTIMES
    makeDirectoryWithLog(BASE_PATH + "downtimes")
    writeSearchFile(BASE_PATH + "downtimes", '["Downtimes"]')

    # GGUS TICKETS
    makeDirectoryWithLog(BASE_PATH + "ggusTickets")
    writeSearchFile(BASE_PATH + "ggusTickets", '["GGUS Tickets"]')

    # NOTICES
    makeDirectoryWithLog(BASE_PATH + "notices")
    writeSearchFile(BASE_PATH + "notices", '["Notices"]')

    # CAPACITY
    for name in CAPACITY_DATA_LABELS:
        makeDirectoryWithLog(BASE_PATH + "capacityOverTime" + name)
        writeSearchFile(BASE_PATH + "capacityOverTime" + name,
                        json.dumps([name]))

    # PLEDGES
    for key in PLEDGES_ROW_DATA_LABELS:
        makeDirectoryWithLog(BASE_PATH + "pledgesOverTime" + key)
        writeSearchFile(BASE_PATH + "pledgesOverTime" + key,
                        json.dumps(PLEDGES_EXPERIMENT_DATA_LABELS))
        makeDirectoryWithLog(BASE_PATH + "pledgesOverTime" + key + "SumOnly")
        writeSearchFile(BASE_PATH + "pledgesOverTime" + key + "SumOnly",
                        json.dumps([PLEDGES_EXPERIMENT_DATA_LABELS[-1]]))

    # STORAGE USAGE
    vo_list = [None, "alice", "atlas", "cms", "lhcb", "hone", "ilc", "mice",
               "minos", "na62", "snoplus", "t2k", "superb", "dirac"]

    for vo in vo_list:
        # store the path to place the folders in
        thisPath = BASE_PATH + "storageUsage"
        # if its the overall VO datasource then add nothing to the path
        # else add the vo's name but capitalized
        thisPath += "" if vo is None else vo.capitalize()
        makeDirectoryWithLog(thisPath)
        # Create the search file content
        searchFileContent = '["Storage Usage Feed '
        searchFileContent += ("Overall"
                              if vo is None else "For " + vo.capitalize())
        searchFileContent += '"]'
        writeSearchFile(thisPath, searchFileContent)
except BaseException as ex:
    logger.exception(ex)
