from __future__ import print_function
import json  # to format the output
import requests  # to get the data
# import the xml parser as a more manageable name
import xml.etree.ElementTree as ET

from utils import writeFileWithLog, createHTMLLinkString

from config import BASE_PATH, URL_GGUS_TICKETS, URL_GGUS_SPECIFIC_TICKET

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# stop it complaining that its not checking certificates

path = BASE_PATH + "ggusTickets"

# get an xml return from this URL and don't check certificates
r = requests.get(URL_GGUS_TICKETS, verify=False)

xmlRoot = ET.fromstring(r.text)
# xml root is the containing tag in the document
# assume the xml is of this form:
'''
<tickets>
    <ticket>
        <request_id>...</request_id>
        <ticket_type>USER</ticket_type>
        <affected_vo>...</affected_vo>
        <affected_site>...</affected_site>
        <responsible_unit>...</responsible_unit>
        <status>...</status>
        <priority>...</priority>
        <priority_color>green</priority_color>
        <date_of_creation>2016-11-07 12:07:00</date_of_creation>
        <last_update>2016-11-07 12:34:00</last_update>
        <type_of_problem>...</type_of_problem>
        <subject>
        ...
        </subject>
    </ticket>
    <ticket> ... </ticket>
    ....
</tickets>
'''
jsonObj = [{"columns": [], "rows": [], "type": "table"}]
# the object which will eventually be converted into JSON

jsonObj[0]["columns"] = [
    # preset the titles of the columns of the table
    {
        "text": "ID"
    },
    {
        "text": "Priority"
    },
    {
        "text": "Status"
    },
    {
        "text": "VO"
    },
    {
        "text": "Problem"
    },
    {
        "text": "Updated"
    },
    {
        "text": "Subject"
    },
    {
        "text": "Code"
    }
]

# xmlRoot[i] is the 'i'th ticket so iterate through the tickets
for xmlTicket in xmlRoot:
    # add the data in order of columns to the jsonObj
    # store the id and status because we use it twice
    storedId = xmlTicket.find("request_id").text
    storedStatus = xmlTicket.find("status").text

    # setup the link here for readability
    linkToTicket = createHTMLLinkString(URL_GGUS_SPECIFIC_TICKET, storedId)

    jsonObj[0]["rows"].append([
        linkToTicket,  # parse the id into an integer
        xmlTicket.find("priority").text,
        storedStatus,
        xmlTicket.find("affected_vo").text,
        xmlTicket.find("type_of_problem").text,
        xmlTicket.find("last_update").text,
        xmlTicket.find("subject").text,
        1 if storedStatus == "assigned" else ""
        # add a code value to help with colouring
        # if not set it to empty string so this cell isn't obvious
    ])

writeFileWithLog(path + "/query", json.dumps(jsonObj))
