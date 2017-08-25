"""This script contains core functions that are used accross multiple
updateX.py scripts. They are imported in each script to avoid repetition.
"""
from __future__ import print_function
import os
import logging
import logging.handlers
from config import LOG_DIR, LOG_FORMAT


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
        print("Created Dir: ", path)


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
            print("You need to run setupFolders.py (which must succeed) "
                  "before trying to write:", filePath)
        else:
            # This isn't expected so raise it!
            raise
    else:
        print("Written file at:", filePath)


def createHTMLLinkString(preFormattedHref, name):
    """Takes a `preFormattedHref` string which contains {0} to be formatted with
    `name` and returns a string which contains the HTML for an <a> link tag to
    this formatted href with the value of name.

    This is included here because it is a function that is repeated in three
    different scripts to create a HTML link in Grafana.
    """
    href = preFormattedHref.format(name)
    return "<a href='{0}'>{1}</a>".format(href, name)


def getLogger():
    """Returns the global logger object used by all scripts.
    If necessary, it sets it up."""
    if not os.path.isdir(LOG_DIR):
        try:
            os.mkdir(LOG_DIR)
        except OSError as ex:
            if ex.args[1] == "File exists":
                pass
    logger = logging.getLogger('StatusJsonDatasource')
    logger.handlers = []  # Remove old handlers - conf may have changed
    # Add a new handler with the current configuration
    thisLogFilePath = os.path.join(LOG_DIR, "log")
    # Use a maximum of 1MB per log file and overwrite after 50 files
    # So use a maximum of 50MB
    fileLogHandler = logging.handlers.RotatingFileHandler(thisLogFilePath, "a",
                                                          maxBytes=1000000,
                                                          backupCount=50)
    fileLogHandler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(fileLogHandler)
    logger.setLevel(logging.INFO)
    return logger
