"""
This is a config file. It is imported by the other scripts so that they can
share the same configuration.
"""

# The base path under which the different datasources are served.
# setupFolders.py creates this path and the sub directories
BASE_PATH = "/var/www/html/grafanaJsonDatasources/"
assert BASE_PATH[-1] == "/"

# The wlcg address where the json for capacity can be obtained.
# {0} is replaced by format() with the year
# {1} is replaced by format() with the month
URL_WLCG_CAPACITIES = ("https://wlcg-rebus.cern.ch/apps/capacities/"
                       "federation_sites/208/{0}/{1}/json_datatables")

# The web address where the xml for downtimes at RAL can be accessed
URL_GOC_DOWNTIMES = ("https://goc.egi.eu/gocdbpi/public/?"
                     "method=get_downtime&topentity=RAL-LCG2")
