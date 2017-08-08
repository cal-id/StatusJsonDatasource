# Mag DB
MAG_DBNAME = "magdb name as a string"
MAG_HOST = "magdb host as a string"
MAG_USER = "magdb username as a string"
MAG_PASSWD = "maddb password as a string"

# ldap
LDAP_HOST = "ldap host as a string"

# noticeboard
# As of 8/8/17, this address was on the STFC private network version of the
# public webserver for http://www.gridpp.rl.ac.uk/status with some additional
# path to get to noticeboard.txt. I am told that this will change...
# Also, currently it is possible to access noticeboard.txt from within STFC
# without a certificate on http:// but not https://.
# This string is passed straight into python's request.get() so make sure to
# use the full address.
NOTICES_ADDRESS = "web accessible address of where noticeboard.txt is stored"
