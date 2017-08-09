from __future__ import print_function
import os

# setup storage usage folders

# store the path to place the folders in
path = "/var/www/html/grafanaJsonDatasources/diskServersInIntervention"

try:
    os.makedirs(path)
    print("Created folder: " + path)
except OSError:
    print("Folder already exists: " + path)
try:
    os.makedirs(path + "HTML")
    print("Created folder: " + path + "HTML")
except OSError:
    print("Folder already exists: " + path + "HTML")

# create this folder

# setup the search file: the search file is the one that is read
# by grafana to create the dropdown box when selecting datasource
with open(path + "/search", "w") as searchFile:
    json = '["Disk Servers in Intervention"]'
    searchFile.write(json)
    print("Written file: " + path + "/search")

with open(path + "HTML/search", "w") as searchFile:
    json = '["Disk Servers in Intervention HTML"]'
    searchFile.write(json)
    print("Written file: " + path + "/search")
from __future__ import print_function
import os  # so that we can make folders

path = "/var/www/html/grafanaJsonDatasources/downtimes"

try:
    os.makedirs(path)
    print("Created folder at: " + path)
except OSError:
    print("Couldn't make folder, folder already exists: " + path)

with open(path + "/search", "w") as fh:
    fh.write('["Downtimes"]')
from __future__ import print_function
import os  # so that we can make folders

path = "/var/www/html/grafanaJsonDatasources/ggusTickets"

try:
    os.makedirs(path)
    print("Created folder at: " + path)
except OSError:
    print("Couldn't make folder, folder already exists: " + path)

with open(path + "/search", "w") as fh:
    fh.write('["GGUS Tickets"]')
from __future__ import print_function
import os  # so that we can make folders

path = "/var/www/html/grafanaJsonDatasources/notices"

try:
    os.makedirs(path)
    print("Created folder at: " + path)
except OSError:
    print("Couldn't make folder, folder already exists: " + path)

with open(path + "/search", "w") as fh:
    fh.write('["Notices"]')
from __future__ import print_function
import os

# setup storage usage folders

vo_list = [
    None, "alice", "atlas", "cms", "lhcb", "hone", "ilc", "mice", "minos",
    "na62", "snoplus", "t2k", "superb", "dirac"
]

for vo in vo_list:
    # store the path to place the folders in
    path = "/var/www/html/grafanaJsonDatasources/storageUsage"
    path += "" if vo is None else vo.capitalize()
    # if its the overall VO datasource then ad nothing to the path
    # else add the vo's name but capitalized
    try:
        os.makedirs(path)
        print("Created Folder: " + path)
    except OSError:
        print("Folder already exists: " + path)
    # create this folder
    # setup the search file: the search file is the one that is read
    # by grafana to create the dropdown box when selecting datasource
    with open(path + "/search", "w") as searchFile:
        text = '["Storage Usage Feed '
        text += "Overall" if vo is None else "For " + vo.capitalize()
        text += '"]'
        searchFile.write(text)
        print("Written file: " + path + "/search")
