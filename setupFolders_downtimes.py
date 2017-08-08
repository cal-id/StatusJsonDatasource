import os  # so that we can make folders

path = "/var/www/html/grafanaJsonDatasources/downtimes"

try:
    os.makedirs(path)
    print("Created folder at: " + path)
except OSError:
    print("Couldn't make folder, folder already exists: " + path)

with open(path + "/search", "w") as fh:
    fh.write('["Downtimes"]')
