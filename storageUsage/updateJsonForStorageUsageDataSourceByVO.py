import ldap # get the ldap module which is what we will use for the data source at the begining
import json # get the json module so that the object can be serialized at the end
from secret import LDAP_HOST
jsonObj = [{"columns":[],"rows":[],"type":"table"}] # the object which will eventually be converted into JSON
jsonObj[0]["columns"]=[{"text": "VO/DiskPool"},{"text": "Disk Used (%)"},{"text": "Disk Used (total)"},{"text": "Disk Total"},{"text": "Tape Used"}] # set the predefined column headings

# this is a list of vos which is copied straight from tiju's code: he chose them
vo_list = ["alice","atlas","cms","lhcb","hone","ilc","mice","minos","na62","snoplus","t2k","superb","dirac"]
for vo in vo_list:
	# go through each vo individually
	ldapObject = ldap.open(LDAP_HOST,2170) # open the ldap server
	ldap.set_option(ldap.OPT_NETWORK_TIMEOUT,3) # set some options. Not sure if this is necessary, Tiju did this in his code

	# below are some options that are used in the search
	dn = "glueseuniqueid=srm-"+vo+".gridpp.rl.ac.uk,mds-vo-name=ral-lcg2,mds-vo-name=local,o=grid"
	fil = "(objectclass=gluese)"
	justThese = ["GlueSETotalOnlineSize","GlueSEUsedOnlineSize","GlueSEUsedNearlineSize","GlueSETotalNearlineSize"]

	# get a searchReference integer and use the ldap module to get the result from the search reference.
	searchReference = ldapObject.search(dn, ldap.SCOPE_SUBTREE, filterstr=fil, attrlist=justThese)
	result = ldapObject.result(searchReference)[1][0][1]

	# result["GlueSEUsedOnlineSize"][0] is disk used
	# result["GlueSETotalOnlineSize"][0] is disk total
	# result["GlueSEUsedNearlineSize"][0] is tape used

	# thisRow should be of the form <vo name> <percentage disk used> <total disk used> <total disk avaliable> <total tape used>
	thisRow = [] # each vo is one row of content, thisRow will eventually be appended onto jsonObj[0]["rows"]
	thisRow.append(vo)
	thisRow.append(int(round(int(result["GlueSEUsedOnlineSize"][0])*100/int(result["GlueSETotalOnlineSize"][0])))) # calculate the percentage to 0dp
	thisRow.append(int(result["GlueSEUsedOnlineSize"][0]))
	thisRow.append(int(result["GlueSETotalOnlineSize"][0]))
	thisRow.append(int(result["GlueSEUsedNearlineSize"][0]))
	jsonObj[0]["rows"].append(thisRow)

try:
	with  open("/var/www/html/grafanaJsonDatasources/storageUsage/query","w") as outputFile: # have to do it this way to ensure that the file system gets cleaned up if there is an error or something
		outputFile.write(json.dumps(jsonObj)) # json.dumps is serializing the object, outputFile.write sends the text to the file
except IOError:
	raise Exception("This folder probably doesn't exist. Try running 'setupFolders.py' from the directory that this python script is run from.")
