"""This script contains core functions that are used accross multiple
updateX.py scripts. They are imported in each script to avoid repetition.
"""
from __future__ import print_function
import os


def makeDirectoryWithLog(path):
    """Creates the folders (including parent folders) for a given path. This
    should log if there was a success or failure."""
    try:
        os.makedirs(path)
    except OSError as ex:
        if ex.args[1] == "Permission denied":
            # In python3.3+ there is a Permission Error but it inherits from
            # OSError
            print("Could not create {0}. You don't have permission!"
                  .format(path))
        elif ex.args[1] == "File exists":
            pass
        else:
            raise
    else:
        print(path, "was created")


def writeFileWithLog(filePath, content):
    """Writes file with path `filePath` using the *text* content `content`.
    """
    try:
        with open(filePath, "w") as searchFile:
            searchFile.write(content)
    # This error is IOError in python2 but OSError in python3
    except (OSError, IOError) as ex:
        if ex.args[1] == "Permission denied":
            print("Could not create {0}. You don't have permission!"
                  .format(filePath))
        if ex.args[1] == "No such file or directory":
            print("You need to run setupFolders.py (which must succeed)"
                  "before trying to write:", filePath)
        else:
            # This isn't expected so raise it!
            raise
    else:
        print("Written file at:", filePath)
