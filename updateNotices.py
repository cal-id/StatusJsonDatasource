import json
# import json so that we can format output
import requests  # To get noticeboard.txt
from secret import NOTICES_ADDRESS
from utils import writeFileWithLog
from config import BASE_PATH

path = BASE_PATH + "notices/query"

jsonObj = [{"columns": [], "rows": [], "type": "table"}]
# the object which will eventually be converted into JSON

jsonObj[0]["columns"] = [
    # preset the titles of the columns of the table
    {
        "text": "Date"
    },
    {
        "text": "Added by"
    },
    {
        "text": "Subject"
    },
    {
        "text": "Description"
    }
]
response = requests.get(NOTICES_ADDRESS)
for line in response.text.split("\n"):  # step through each line in the file
    if line not in "\n\r":
        cols = line.split(";")  # split each line into cols

        # for example a cols would look like this:
        # [
        #     '1252589462',
        #     'Tiju Idiculla',
        #     '/C=UK/O=eScience/OU=CLRC/L=RAL/CN=tiju idiculla',
        #     'Castor Database problems',
        #     'There are some problems on the CMS and GEN instances of the
        #     Castor database. The problem is under investigation.\n'
        # ]

        jsonObj[0]["rows"].append([
            # parse the timestamp into an integer and change into
            # miliseconds
            int(cols[0]) * 1000,
            cols[1],  # ignore the certificate
            cols[3],
            cols[4]
        ])

writeFileWithLog(path, json.dumps(jsonObj))
