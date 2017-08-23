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
# This is used in updateCapacity.py
URL_WLCG_CAPACITIES = ("https://wlcg-rebus.cern.ch/apps/capacities/"
                       "federation_sites/208/{0}/{1}/json_datatables")

# The web address for GOCDB where the xml for downtimes at RAL can be accessed
# This is used in updateDowntimes.py
URL_GOC_DOWNTIMES = ("https://goc.egi.eu/gocdbpi/public/?"
                     "method=get_downtime&topentity=RAL-LCG2")

# The web address which will link through to more information about a specific
# GOCDB downtime id.
# {0} is replaced by format() with the specific downtime id
# This is used in updateDowntimes.py
URL_GOC_SPECIFIC_DOWNTIME = ("https://goc.egi.eu/portal/index.php?"
                             "Page_Type=Downtime&id={0}")
