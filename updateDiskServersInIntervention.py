from __future__ import print_function
from pg import DB  # from PyGreSQL import database function
from secret import MAG_DBNAME, MAG_HOST, MAG_USER, MAG_PASSWD
from config import BASE_PATH, URL_OVERWATCH_MACHINE_NAME
import json
# get the json module so that the object can be serialized at the end

from utils import writeFileWithLog

db = DB(dbname=MAG_DBNAME, host=MAG_HOST, user=MAG_USER, passwd=MAG_PASSWD)
# log into the database as the object db

listOfSelectValues = ["machineName", "virtualOrganisation", "diskPool", "dxtx"]
# list of data to get from the database about each diskserver in intevention.
# For now this is also a list of column headings
'''
List of possible items to select for each diskserver.
At the moment, I am just going with the ones that Tiju had.

virtualOrganisation
diskPool
serviceType
numberFileSystems
machineName
sizeTb
miscComments
currentTeam
hardwareGroup
castorInstance
lastVerified
currentStatus
dxtx
normalStatus
puppetManaged
quattorManaged
'''

assert len(listOfSelectValues) != 0
# throw an error if there are no select values
# set up the begining of the query string (before adding the select values)
queryString = 'SELECT '

queryString += '"' + listOfSelectValues[0] + '"'  # add the first of the select
# values (already threw an error if this doesn't exist)

for selectValue in listOfSelectValues:
    # add the rest of the select values with a comma for separation
    # (if there even are any)
    queryString += ', "' + selectValue + '"'

# finish the end of the query string
queryString += (' from "vCastor" '
                'where ("virtualOrganisation" != \'n/a\' '
                'and "virtualOrganisation" != \'vcert2\' '
                'and "currentStatus" != \'Production\' '
                'and  "currentStatus" != \'Draining\' '
                'and  "currentStatus" != \'ReadOnly\') '
                'and ("normalStatus" = \'Production\' '
                'OR "normalStatus" = \'ReadOnly\') '
                'order by "virtualOrganisation"')
# example of a valid query string:
# 'SELECT "machineName", "virtualOrganisation", "diskPool",  "dxtx"
# from "vCastor"
# where ("virtualOrganisation" != \'n/a\'
# and "virtualOrganisation" != \'vcert2\'
# and "currentStatus" != \'Production\'
# and  "currentStatus" != \'Draining\'
# and  "currentStatus" != \'ReadOnly\')
# and ("normalStatus" = \'Production\'
# OR "normalStatus" = \'ReadOnly\')
# order by "virtualOrganisation"'

# get a query object
query = db.query(queryString)

listOfResults = query.dictresult()
# this is a list of dictionaries which have keys defined by the select values
# above
# an example of a return (only one item in list):
# [{'virtualOrganisation': 'Facilities', 'machineName': 'fdsdss36', 'dxtx':
# 'd1t0', 'diskPool': 'cedaDiskTest'}]

jsonObj = [{"columns": [], "rows": [], "type": "table"}]
# the object which will eventually be converted into JSON

jsonObj[0]["columns"] = [{"text": key} for key in listOfSelectValues]
# set the predefined column based on the select values for the moment

if "diskPool" in listOfSelectValues:
    # if there is a diskpool column then we can add a Space Token column after
    # the diskpool
    jsonObj[0]["columns"].insert(
        listOfSelectValues.index("diskPool") + 1, {"text": "Space Token"})

# a mapping from disk pool to machine name
# so spacetoken = spaceTokenMap[diskPool]
# this comes straight out of Tiju's code but translated into python dictionary
spaceTokenMap = {
    "atlasFarm": "",
    "atlasHotDisk": "",
    "atlasNonProd": "",
    "atlasScratchDisk": "ATLASSCRATCHDISK",
    "atlasSimRaw": "ATLASMCTAPE",
    "atlasSimStrip": "ATLASMCDISK",
    "atlasSpare": "",
    "atlasStripDeg": "ATLASGROUPDISK",
    "atlasStripInput": "ATLASDATADISK",
    "atlasT0Raw": "ATLASDATATAPE",
    "atlasTape": "ATLASDATATAPE",
    # TODO: cedaDiskTest is NOT in this mapping...
    "cmsFarmRead": "cmsFarmRead",
    "cmsSpare": "",
    "cmsTest": "",
    "cmsDisk": "",
    "cmsTape": "",
    "cmsWanIn": "CMS_DEFAULT",
    "cmsWanOut": "cmsWanOut",
    "lhcbDst": "LHCb_DST",
    "lhcbMdst": "LHCb_M-DST",
    "lhcbNonProd": "",
    "lhcbRawRdst": "LHCb_RAW",
    "lhcbSpare": "",
    "lhcbUser": "",
    "aliceTape": "",
    "dteamTest": "",
    "genNonProd": "",
    "genTape": "",
    "genTest": "",
    "xrootd": "xrootd",
    "NFS": "NFS",
    "upgrade": ""
}

for item in listOfResults:
    thisRow = []
    # each item is one row of content
    # thisRow will eventually by appended to jsonObj
    for selectValue in listOfSelectValues:
        try:
            toAppend = item[selectValue]
        except KeyError:
            # if there is a key error then it wasn't returned from the database
            # for the moment this means just print a blank row
            # TODO: this should be logged or something
            toAppend = ""
        thisRow.append(toAppend)
        if selectValue == "diskPool":
            # if we are in the diskPool column then we need to add a column for
            # space token
            try:
                thisRow.append(spaceTokenMap[toAppend])
            except KeyError:
                # if there isnt a mapping this is probably a problem so log
                # this
                # TODO: log this
                # For the moment we can just assume no spacetoken for this
                # diskpool
                thisRow.append("")

    jsonObj[0]["rows"].append(thisRow)

writeFileWithLog(BASE_PATH + "diskServersInIntervention/query",
                 json.dumps(jsonObj))

# do the HTML version as well. This one formats the machine name with a link
# which goes through to
# https://overwatch.gridpp.rl.ac.uk/index.php?view:system:
if "machineName" in listOfSelectValues:
    colIndex = listOfSelectValues.index("machineName")
    # find which col is machine name so that we can edit that
    for row in jsonObj[0]["rows"]:
        # go through each row and change the value of the machine name col to a
        # html link
        machineName = row[colIndex]
        href = URL_OVERWATCH_MACHINE_NAME.format(machineName)
        row[colIndex] = ("<a href='{0}'>{1}</a>").format(href, machineName)

    writeFileWithLog(BASE_PATH + "diskServersInInterventionHTML/query",
                     json.dumps(jsonObj))
