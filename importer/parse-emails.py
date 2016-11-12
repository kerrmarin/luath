#!/usr/bin/env python

import os, argparse, sys, json, credentials

from Email import Email
from EmailParser import EmailParser
from EmailConverter import EmailConverter
from datetime import datetime
from PGSQLExporter import PGSQLExporter, PGSQLConfiguration

def parseEmailsFromDirectory(directory):
    """
    Traverses a directory of zipped files containing emails and extracts the
    email messages from them
    """
    email_messages = {}
    parser = EmailParser()
    files = os.listdir(directory)

    fullpaths = [os.path.join(directory, fi) for fi in files]

    print "Parsing emails...",
    for path in fullpaths:
        print "\b.",
        sys.stdout.flush()
        email_messages[path] = parser.parse(path)
    print "\nAll messages parsed"
    return email_messages

def getDirectoryFromArguments():
    """
    Gets the directory argument from the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory',
                        help='Directory to traverse for zipped files \
                        with emails in text format',
                        required=True)
    args = parser.parse_args()
    return args.directory

if __name__ == "__main__":
    directory = getDirectoryFromArguments()
    messages = parseEmailsFromDirectory(directory)
    emailConverter = EmailConverter()
    configuration = PGSQLConfiguration(credentials.db_host,
                                        credentials.db_username,
                                        credentials.db_password,
                                        credentials.db_database)
    exporter = PGSQLExporter(configuration)
    for path, messagelist in messages.items():
        emails = emailConverter.convertEmailsFromMessages(messagelist)
        exporter.export(emails)
    for path, messagelist in messages.items():
        emails = emailConverter.convertEmailsFromMessages(messagelist)
        exporter.addReferences(emails)
    exporter.closeConnection()
