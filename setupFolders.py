"""
This script sets up the folders for some of the datasources:
- Disk Servers In Intervention
- Downtimes
- GGUS Tickets
- Notices
- Storage Usage (this has an overall datasource AND one per VO)

For each data source, it creates a top directory:
    BASE_PATH + "something_to_identify_the_datasource"

And a search file with in this top directory. This file is downloaded by
Grafana to give it the titles of the data in this URL.

Works with python2 or python3
"""

from __future__ import print_function
import os
from utils import writeFileWithLog
from config import BASE_PATH


# INITIAL SETUP
def makeDirectoryWithLog(path):
    """Creates the folders (including parent folders) for a given path. This
    should log if there was a success or failure."""
    try:
        os.makedirs(path)
    except OSError as ex:
        if ex.args[1] == "Permission denied":
            # In python3.3+ there is a Permission Error but it inherits from
            # OSError
            print("Could not create {}. You don't have permission!"
                  .format(path))
        elif ex.args[1] == "File exists":
            pass
        else:
            raise
    else:
        print(path, "was created")


def writeSearchFile(path, content):
    """Writes content (string) to a new file 'search' located under path.
    eg /var/www/html/grafanaJsonDatasources/diskServersInIntervention
    writes content to
    /var/www/html/grafanaJsonDatasources/diskServersInIntervention/search
    """
    filePath = os.path.join(path, "search")
    writeFileWithLog(filePath, content)


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
    searchFileContent += "Overall" if vo is None else "For " + vo.capitalize()
    searchFileContent += '"]'
    writeSearchFile(thisPath, searchFileContent)
