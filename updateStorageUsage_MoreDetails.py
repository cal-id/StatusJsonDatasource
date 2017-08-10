from __future__ import print_function

import sys  # to check py3 vs py2
from utils import writeFileWithLog
import ldap  # get the ldap module which is what we will use for the data
# source at the begining
import json  # get the json module so that the object can be serialized at the
# end
from secret import LDAP_HOST
from config import BASE_PATH
vo_list = [
    "alice", "atlas", "cms", "lhcb", "hone", "ilc", "mice", "minos", "na62",
    "snoplus", "t2k", "superb", "dirac"
]  # this is the list of vos to go through

for vo in vo_list:
    jsonObj = [{
        "columns": [],
        "rows": [],
        "type": "table"
    }]  # the object which will eventually be converted into JSON
    jsonObj[0]["columns"] = [{
        "text": "VO/DiskPool"
    }, {
        "text": "Disk Used (%)"
    }, {
        "text": "Disk Used (total)"
    }, {
        "text": "Disk Free"
    }, {
        "text": "Disk Total"
    }, {
        "text": "Tape Used"
    }]  # set the predefined column headings

    # open the ldap server
    ldapObject = ldap.open(LDAP_HOST, 2170)
    ldap.set_option(
        ldap.OPT_NETWORK_TIMEOUT, 3
    )  # set some options. Not sure if this is necessary, Tiju did this in his
    # code

    # below are some options that are used in the search
    dn = ("glueseuniqueid=srm-" + vo +
          ".gridpp.rl.ac.uk,mds-vo-name=ral-lcg2,mds-vo-name=local,o=grid")
    fil = "(objectclass=gluesa)"
    justThese = [
        "GlueSATotalOnlineSize", "GlueSAUsedOnlineSize",
        "GlueSAFreeOnlineSize", "GlueSALocalID", "GlueSATotalNearlineSize",
        "glueSAusednearlinesize", "GlueSAFreeNearlineSize"
    ]

    # get a searchReference integer and use the ldap module to get the result
    # from the search reference.
    searchReference = ldapObject.search(
        dn, ldap.SCOPE_SUBTREE, filterstr=fil, attrlist=justThese)
    rows = ldapObject.result(searchReference)[1]
    # rows is a list of dictionaries like below. I think each row is called a
    # 'Disk Pool'
    # {'GlueSATotalNearlineSize': ['1441'], 'GlueSATotalOnlineSize': ['11183'],
    # 'GlueSAUsedNearlineSize': ['303'], 'GlueSAUsedOnlineSize': ['8352'],
    # 'GlueSAFreeOnlineSize': ['2830'], 'GlueSAFreeNearlineSize': ['1137'],
    # 'GlueSALocalID': ['genTape']}

    for row in rows:
        # thisRow should be of the form <diskpool> <percentage disk used>
        # <total disk used> <disk free> <total disk avaliable>
        # <total tape used>
        thisRow = []
        # each vo is one row of content, thisRow will eventually be appended
        # onto jsonObj[0]["rows"]
        # row[1]['GlueSALocalID'][0] is diskpool name
        # TODO: is this the correct term?
        # row[1]['GlueSAUsedOnlineSize'][0] is Disk Used
        # row[1]['GlueSAFreeOnlineSize'][0] is Disk Free
        # row[1]['GlueSATotalOnlineSize'][0] is Disk Total
        # row[1]['GlueSAUsedNearlineSize'][0] is Tape Used
        localId = (row[1]['GlueSALocalID'][0] if sys.version_info < (3,)
                   else row[1]['GlueSALocalID'][0].decode())
        # If this is python3, the localId is in bytes form. We need a
        # string to encode to JSON.
        thisRow.append(localId)
        try:
            thisRow.append(int(round(
                int(row[1]['GlueSAUsedOnlineSize'][0]) * 100 /
                int(row[1]['GlueSATotalOnlineSize'][0]))))
        except ZeroDivisionError:
            print("Got zero online size for vo: {} at {}"
                  .format(vo, localId))
            thisRow.append(0)
        thisRow.append(int(row[1]['GlueSAUsedOnlineSize'][0]))
        thisRow.append(int(row[1]['GlueSAFreeOnlineSize'][0]))
        thisRow.append(int(row[1]['GlueSATotalOnlineSize'][0]))
        thisRow.append(int(row[1]['GlueSAUsedNearlineSize'][0]))
        jsonObj[0]["rows"].append(thisRow)

    writeFileWithLog(BASE_PATH + "storageUsage" + vo.capitalize() + "/query",
                     json.dumps(jsonObj))
