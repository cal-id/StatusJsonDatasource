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
