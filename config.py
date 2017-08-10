"""
This is a config file. It is imported by the other scripts so that they can
share the same configuration.
"""

# The base path under which the different datasources are served.
# setupFolders.py creates this path and the sub directories
BASE_PATH = "/var/www/html/grafanaJsonDatasources/"
assert BASE_PATH[-1] == "/"
