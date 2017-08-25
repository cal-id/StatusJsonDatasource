# get the ldap module which is what we will use for the data source
import ldap
from utils import writeFileWithLog, getLogger
import json  # get the json module for serializing
from secret import LDAP_HOST
from config import BASE_PATH

logger = getLogger()
logger.debug("Starting")

jsonObj = [{
    "columns": [],
    "rows": [],
    "type": "table"
}]  # the object which will eventually be converted into JSON
# set the predefined column headings
jsonObj[0]["columns"] = [{"text": "VO/DiskPool"},
                         {"text": "Disk Used (%)"},
                         {"text": "Disk Used (total)"},
                         {"text": "Disk Total"},
                         {"text": "Tape Used"}]

# this is a list of vos which is copied straight from tiju's code:
# he chose them
vo_list = [
    "alice", "atlas", "cms", "lhcb", "hone", "ilc", "mice", "minos", "na62",
    "snoplus", "t2k", "superb", "dirac"
]

# open the ldap server
ldapObject = ldap.open(LDAP_HOST, 2170)
ldap.set_option(
    ldap.OPT_NETWORK_TIMEOUT, 3
)  # set some options. Not sure if this is necessary,
# Tiju did this in his code
logger.debug("LDAP connection established")

for vo in vo_list:
    # go through each vo individually
    # below are some options that are used in the search
    dn = ("glueseuniqueid=srm-" + vo +
          ".gridpp.rl.ac.uk,mds-vo-name=ral-lcg2,mds-vo-name=local,o=grid")
    fil = "(objectclass=gluese)"
    justThese = [
        "GlueSETotalOnlineSize", "GlueSEUsedOnlineSize",
        "GlueSEUsedNearlineSize", "GlueSETotalNearlineSize"
    ]

    # get a searchReference integer and use the ldap module to get the result
    # from the search reference.
    searchReference = ldapObject.search(
        dn, ldap.SCOPE_SUBTREE, filterstr=fil, attrlist=justThese)
    result = ldapObject.result(searchReference)[1][0][1]
    logger.debug("LDAP serach returned for vo: {0}".format(vo))

    # result["GlueSEUsedOnlineSize"][0] is disk used
    # result["GlueSETotalOnlineSize"][0] is disk total
    # result["GlueSEUsedNearlineSize"][0] is tape used

    # thisRow should be of the form <vo name> <percentage disk used>
    # <total disk used> <total disk avaliable> <total tape used>
    thisRow = []
    # each vo is one row of content, thisRow will eventually be appended
    # onto jsonObj[0]["rows"]
    thisRow.append(vo)
    thisRow.append(
        int(
            round(
                int(result["GlueSEUsedOnlineSize"][0]) * 100 / int(
                    result["GlueSETotalOnlineSize"][
                        0]))))  # calculate the percentage to 0dp
    thisRow.append(int(result["GlueSEUsedOnlineSize"][0]))
    thisRow.append(int(result["GlueSETotalOnlineSize"][0]))
    thisRow.append(int(result["GlueSEUsedNearlineSize"][0]))
    jsonObj[0]["rows"].append(thisRow)

writeFileWithLog(BASE_PATH + "storageUsage/query", json.dumps(jsonObj))
logger.debug("Written JSON Data")
