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
"""

from __future__ import print_function
import os
import sys

# INITIAL SETUP

BASE_PATH = "/var/www/html/grafanaJsonDatasources/"
assert BASE_PATH[-1] == "/"


def makeDirectoryWithLog(path):
    """Creates the folders (including parent folders) for a given path. This
    should log if there was a success or failure."""
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as ex:
        if sys.version_info < (3, 3) or isinstance(ex, PermissionError):
            # In python3.3+ there is the concept of a Permission Error
            print("Could not create {}. You don't have permission!"
                  .format(path))
    except BaseException as ex:
        print("Failed to create {} with an unexpected error!".format(path))
        raise
    else:
        print(path, "is available")


def writeSearchFile(path, content):
    """Writes content (string) to a new file 'search' located under path.
    eg /var/www/html/grafanaJsonDatasources/diskServersInIntervention
    writes content to
    /var/www/html/grafanaJsonDatasources/diskServersInIntervention/search
    """
    filePath = os.path.join(path, "search")
    try:
        with open(filePath, "w") as searchFile:
            searchFile.write(content)
            print("Written file:", filePath)
    except OSError as ex:
        if sys.version_info < (3, 3) or isinstance(ex, PermissionError):
            # In python3.3+ there is the concept of a Permission Error
            print("Could not create {}. You don't have permission!"
                  .format(filePath))
    except BaseException as ex:
        print("Failed to create {} with an unexpected error!".format(path))
        raise
    else:
        print(path, "is available")


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
    makeDirectoryWithLog(thisPath, searchFileContent)