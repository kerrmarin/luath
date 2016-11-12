#!/usr/bin/env python

import os, math, argparse
from urllib2 import urlopen, URLError, HTTPError
from datetime import datetime, timedelta, date

def emailLists():
    """
    Returns the lists that will be retrieved from the archive
    """
    return [
        "swift-lldb-dev",
        "swift-build-dev",
        "swift-corelibs-dev",
        "swift-dev",
        "swift-evolution"
    ]

def initialDate():
    """
    Returns the initial date in which the email lists are available in the archives
    """
    return date(2015, 11, 30)

def numberOfWeeks():
    """
    Gets the number of weeks between the current date and the initial date that
    the email list archives are available
    """
    d0 = initialDate()
    d1 = date.today()
    delta = d1 - d0
    return int(math.floor(delta.days / 7))

def getDirectoryFromArguments():
    """
    Gets the directory argument from the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory',
                        help='Directory to save all downloaded files to.\
                        This directory must exist.',
                        required=True)
    args = parser.parse_args()
    return args.directory

if __name__ == "__main__":
    directory = getDirectoryFromArguments()
    if not os.path.isdir(directory):
        print "%s not a directory, or doesn't exist"
        exit()

    lists = emailLists()
    numberOfWeeks = numberOfWeeks()
    for listname in lists:
        currentDate = initialDate()
        for index in range(0, numberOfWeeks + 1):
            try:
                datestring = currentDate.strftime("%Y%m%d")
                url = "https://lists.swift.org/pipermail/%s/Week-of-Mon-%s.txt.gz" % (listname, datestring)
                remotefile = urlopen(url)
                print "Downloading " + url

                # Open our local file for writing
                filename = "%s-%s.txt.gz" % (listname, datestring)
                with open(os.path.join(directory, filename), "wb") as localfile:
                    localfile.write(remotefile.read())

            #handle errors
            except HTTPError, e:
                print "HTTP Error:", e.code, url
            except URLError, e:
                print "URL Error:", e.reason, url
            finally:
                currentDate = currentDate + timedelta(days=7)
