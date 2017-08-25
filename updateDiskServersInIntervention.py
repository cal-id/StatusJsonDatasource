from pg import DB  # from PyGreSQL import database function
from secret import MAG_DBNAME, MAG_HOST, MAG_USER, MAG_PASSWD
from config import BASE_PATH, URL_OVERWATCH_MACHINE_NAME, SPACE_TOKEN_MAP
import json  # For formatting the output
from utils import writeFileWithLog, createHTMLLinkString, getLogger

logger = getLogger()

# log into the database as the object db
db = DB(dbname=MAG_DBNAME, host=MAG_HOST, user=MAG_USER, passwd=MAG_PASSWD)

# List of data to get from the database about each diskserver in intevention.
# For now this is also a list of column headings
listOfSelectValues = ["machineName", "virtualOrganisation", "diskPool", "dxtx"]

# Throw an error if there are no select values
assert len(listOfSelectValues) > 0

queryString = ('SELECT {0} '
               'from "vCastor" '
               'where ("virtualOrganisation" != \'n/a\' '
               'and "virtualOrganisation" != \'vcert2\' '
               'and "currentStatus" != \'Production\' '
               'and  "currentStatus" != \'Draining\' '
               'and  "currentStatus" != \'ReadOnly\') '
               'and ("normalStatus" = \'Production\' '
               'OR "normalStatus" = \'ReadOnly\') '
               'order by "virtualOrganisation"'
               ).format('"' + '", "'.join(listOfSelectValues) + '"')

# get a query object
query = db.query(queryString)

# this is a list of dictionaries which have keys defined by the select values
# above
# an example of a return (only one item in list):
# [{'virtualOrganisation': 'Facilities', 'machineName': 'fdsdss36', 'dxtx':
# 'd1t0', 'diskPool': 'cedaDiskTest'}]
listOfResults = query.dictresult()

# the object which will eventually be converted into JSON
jsonObj = [{"columns": [], "rows": [], "type": "table"}]

# set the predefined column based on the select values for the moment
jsonObj[0]["columns"] = [{"text": key} for key in listOfSelectValues]

if "diskPool" in listOfSelectValues:
    # if there is a diskpool column then we can add a Space Token column after
    # the diskpool
    jsonObj[0]["columns"].insert(listOfSelectValues.index("diskPool") + 1,
                                 {"text": "Space Token"})

for item in listOfResults:
    thisRow = []
    # each item is one row of content
    # thisRow will eventually by appended to jsonObj
    for selectValue in listOfSelectValues:
        try:
            toAppend = item[selectValue]
        except KeyError:
            # if there is a key error then it wasn't returned from the database
            # for the moment this means just use a blank row
            toAppend = ""
            logger.warning(("{0} was not returned from magdb - leaving this "
                            "blank.").format(selectValue))
        thisRow.append(toAppend)
        if selectValue == "diskPool":
            # if we are in the diskPool column then we need to add a column for
            # space token
            try:
                thisRow.append(SPACE_TOKEN_MAP[toAppend])
            except KeyError:
                # if there isnt a mapping this is probably a problem so log
                # this
                # For the moment we can just assume no spacetoken for this
                # diskpool
                thisRow.append("")
                logger.info(("No spacetoken for this diskpool: {0} - leaving "
                             "this blank.").format(toAppend))

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
        row[colIndex] = createHTMLLinkString(URL_OVERWATCH_MACHINE_NAME,
                                             machineName)

    writeFileWithLog(BASE_PATH + "diskServersInInterventionHTML/query",
                     json.dumps(jsonObj))
