import os

# setup storage usage folders

vo_list = [
    None, "alice", "atlas", "cms", "lhcb", "hone", "ilc", "mice", "minos",
    "na62", "snoplus", "t2k", "superb", "dirac"
]

for vo in vo_list:
    # store the path to place the folders in
    path = "/var/www/html/grafanaJsonDatasources/storageUsage"
    path += "" if vo == None else vo.capitalize()
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
        text += "Overall" if vo == None else "For " + vo.capitalize()
        text += '"]'
        searchFile.write(text)
        print("Written file: " + path + "/search")
