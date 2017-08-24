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

# The wlcg address where the json for pledges can be obtained.
# {0} is replaced by format() with the year
# This is used in updatePledges.py
URL_WLCG_PLEDGES = ("http://wlcg-rebus.cern.ch/apps/pledges/resources/"
                    "federation/208/{0}/json_datatables")

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

# The web address to link through to a specific machine in overwatch
# {0} is replaced by format() with machineName returned by magdb
# This is used in updateDiskServersInIntervention.py
URL_OVERWATCH_MACHINE_NAME = ("https://overwatch.gridpp.rl.ac.uk/index.php?"
                              "view:system:{0}")

# The web address to get xml formatted GGUS tickets
# This is used in updateGgusTickets.py
URL_GGUS_TICKETS = ("https://ggus.eu/?mode=ticket_search&"
                    "show_columns_check%5B%5D=AFFECTED_VO&"
                    "show_columns_check%5B%5D=TICKET_TYPE&"
                    "show_columns_check%5B%5D=AFFECTED_SITE&"
                    "show_columns_check%5B%5D=PRIORITY&"
                    "show_columns_check%5B%5D=RESPONSIBLE_UNIT&"
                    "show_columns_check%5B%5D=STATUS&"
                    "show_columns_check%5B%5D=DATE_OF_CHANGE&"
                    "show_columns_check%5B%5D=SHORT_DESCRIPTION&"
                    "ticket_id=&"
                    "supportunit=&"
                    "su_hierarchy=0&"
                    "vo=&"
                    "user=&"
                    "keyword=&"
                    "involvedsupporter=&"
                    "assignedto=&"
                    "affectedsite=RAL-LCG2&"
                    "specattrib=none&"
                    "status=open&"
                    "priority=&"
                    "typeofproblem=&"
                    "ticket_category=all&"
                    "mouarea=&"
                    "date_type=creation+date&"
                    "tf_radio=1&"
                    "timeframe=any&"
                    "untouched_date=&"
                    "orderticketsby=REQUEST_ID&"
                    "orderhow=desc&"
                    "search_submit=GO%21&"
                    "writeFormat=XML")

# The webaddress to link through to more information about a specific ggus
# ticket.
# {0} is replaced by format() with the ggus ticket id
# This is used in updateGgusTickets.py
URL_GGUS_SPECIFIC_TICKET = ("https://ggus.eu/index.php?"
                            "mode=ticket_info&amp;ticket_id={0}")

# The return from a WLCG capacity query looks like this:
# {"aaData": [["EGI", "RAL-LCG2", 1660, 9472, 88781, 8909805, 10264504]]}
# This list specifies the labels of the data [2:]
# For example ["Physical CPU", "Logical CPU", "HEPSPEC06", "Disk", "Tape"]
# Would specify:
#   - 1660         Physical CPU
#   - 9472         Logical CPU
#   - 88781        HEPSPEC06
#   - 8909805      DISK
#   - 10264504     TAPE
CAPACITY_DATA_LABELS = ["Physical CPU", "Logical CPU", "HEPSPEC06", "Disk",
                        "Tape"]

# The return from a WLCG pledges query contains three rows of data. This
# list should contain the first word of the first element in each row.
PLEDGES_ROW_DATA_LABELS = ["CPU", "Disk", "Tape"]

# The return from a WLCG pledges query contains five groups of four in each row
# after the row header (first element). This list gives the lables for each of
# those five sections of data.
# For example ["ALICE", "ATLAS", "CMS", "LHCb", "SUM"] says that
# indicies 1-4 refer to the alice experiment
# indicies 5-8 refer to the atlas experiment
# indicies 9-12 etc..
PLEDGES_EXPERIMENT_DATA_LABELS = ["ALICE", "ATLAS", "CMS", "LHCb", "SUM"]
