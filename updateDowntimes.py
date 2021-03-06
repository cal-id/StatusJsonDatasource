import json  # to format the output
import requests  # to get the data
import xml.etree.ElementTree as ET
# import the xml parser as a more manageable name
import time  # so we can tell if a downtime is ongoin
from config import BASE_PATH, URL_GOC_DOWNTIMES, URL_GOC_SPECIFIC_DOWNTIME
from utils import writeFileWithLog, createHTMLLinkString, getLogger
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# stop it complaining that its not checking certificates

logger = getLogger()
logger.debug("Starting")

try:
    path = BASE_PATH + "downtimes"

    # get an xml return from this URL and don't check certificates
    r = requests.get(URL_GOC_DOWNTIMES, verify=False)
    logger.debug("GOCDB returned successfully")

    xmlRoot = ET.fromstring(r.text)
    logger.debug("Parsed XML successfully")
    # xml root is the containing tag in the document
    # assume the xml is of this form:
    '''
    <results>
        <DOWNTIME ID="..." PRIMARY_KEY="..." CLASSIFICATION="SCHEDULED">...
            </DOWNTIME>
        <DOWNTIME ID="..." PRIMARY_KEY="..." CLASSIFICATION="SCHEDULED">
            <PRIMARY_KEY>100475G0</PRIMARY_KEY>
            <HOSTNAME>...</HOSTNAME>
            <SERVICE_TYPE>XRootD</SERVICE_TYPE>
            <ENDPOINT>...XRootD</ENDPOINT>
            <HOSTED_BY>RAL-LCG2</HOSTED_BY>
            <GOCDB_PORTAL_URL>
            https://goc.egi.eu/portal/index.php?Page_Type=Downtime&id=21902
            </GOCDB_PORTAL_URL>
            <AFFECTED_ENDPOINTS/>
            <SEVERITY>OUTAGE</SEVERITY>
            <DESCRIPTION>
            ...
            </DESCRIPTION>
            <INSERT_DATE>1478617834</INSERT_DATE>
            <START_DATE>1479292200</START_DATE>
            <END_DATE>1479306600</END_DATE>
            <FORMATED_START_DATE>2016-11-16 10:30</FORMATED_START_DATE>
            <FORMATED_END_DATE>2016-11-16 14:30</FORMATED_END_DATE>
        </DOWNTIME>
        ...
    <results>
    '''
    jsonObj = [{"columns": [], "rows": [], "type": "table"}]
    # the object which will eventually be converted into JSON

    jsonObj[0]["columns"] = [
        # preset the titles of the columns of the table
        {"text": "ID"},
        {"text": "Hosts"},
        {"text": "Start"},
        {"text": "End"},
        {"text": "Severity"},
        {"text": "Description"},
        {"text": "Code"}
    ]

    listOfEncounteredDowntimeIds = []
    # this is a list of downtime ids that we have seen before

    dictionaryOfDowntimeIdAgainstRows = {}
    # this is a dictionary that maps the string id of a downtime entry with the
    # list of rows which will go into the jsonObj for the table

    # xmlRoot[i] is the 'i'th downtime so iterate through the downtimes
    for downtimeEntry in xmlRoot:
        dtID = downtimeEntry.attrib["ID"]
        # name downtime id something more useable

        # store the start and end timestamps so they can be used to calculate
        # whether the current downtime is ongoing
        startTime = int(downtimeEntry.find("START_DATE").text)
        endTime = int(downtimeEntry.find("END_DATE").text)
        code = (1 if startTime > time.time()
                else "" if endTime < time.time() else 2)
        # the code is 2 if ongoing, 1 if future

        if dtID not in listOfEncounteredDowntimeIds:
            # note that multiple downtime attributes can have the same id
            # this IF statement deals with the case where there is a downtime
            # with an id that we haven't seen before in which case, that id
            # needs to be added to the list of downtime ids
            listOfEncounteredDowntimeIds.append(dtID)

            dictionaryOfDowntimeIdAgainstRows[dtID] = [
                # make the id a link to more info
                createHTMLLinkString(URL_GOC_SPECIFIC_DOWNTIME, dtID),
                # find the first tag 'HOSTNAME'
                # set it to be in the hosts column provided that the downtime
                # is ongoing or in the future
                (downtimeEntry.find("HOSTNAME").text
                 if code != "" else "See link for more info"),
                startTime * 1000,  # convert to milisecond timestamps
                startTime * 1000,
                (downtimeEntry.attrib["CLASSIFICATION"] + " " +
                 downtimeEntry.find("SEVERITY").text
                 ),
                downtimeEntry.find("DESCRIPTION").text,
                code
            ]
            # set up the entry in the dictionary for this downtime

        elif code != "":
            # if this id has been seen before and it isnt in the past then we
            # should append the additional hosts to the table hostname to the
            # relevant column, the rest of the data is the same between
            # downtimes with the same id
            dictionaryOfDowntimeIdAgainstRows[dtID][1] += "<br />" \
             + downtimeEntry.find("HOSTNAME").text

    for key in dictionaryOfDowntimeIdAgainstRows:
        jsonObj[0]["rows"].append(dictionaryOfDowntimeIdAgainstRows[key])

    writeFileWithLog(path + "/query", json.dumps(jsonObj))
    logger.debug("Written JSON data")
except BaseException as ex:
    logger.exception(ex)
