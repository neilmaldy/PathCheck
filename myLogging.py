__author__ = 'mneil'

import sys
import time

def printToLog(logString):
    """ Print to log file (stderr)
    Prints the logString to stderr, prepends date and time
    """
    print >> sys.stderr, time.strftime("%Y%m%d-%H:%M:%S") + ": " + logString
