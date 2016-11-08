import os, sys, datetime, imaplib
from GmailConverter import GmailConverter
from GmailFetcher import GmailFetcher
from PGSQLExporter import PGSQLConfiguration
from PGSQLExporter import PGSQLExporter

fetcher = GmailFetcher()
mailbox = imaplib.IMAP4_SSL('imap.gmail.com')
lists = [
    "swift-dev@swift.org",
    "swift-build-dev@swift.org",
    "swift-corelibs-dev@swift.org",
    "swift-evolution@swift.org",
    "swift-lldb-dev@swift.org"
]
email = os.environ['gmail_username']
email_password =  os.environ['gmail_password']
if not fetcher.login(email, email_password):
    sys.exit(1)

host = os.environ['db_host']
username = os.environ['db_username']
password = os.environ['db_password']
database = os.environ['db_name']
configuration = PGSQLConfiguration(host,
                                   username,
                                   password,
                                   database)
exporter = PGSQLExporter(configuration)

try:
    if not fetcher.selectFolder(credentials.folder):
        print "Folder selection unsuccessful"
        mailbox.logout()
        sys.exit(1)
    messages = fetcher.fetchEmails()
    filtered = [x for x in messages if x.get("X-Original-To") in lists]
    emailconverter = GmailConverter()
    emails = emailconverter.convertEmailsFromMessages(filtered)
    exporter.export(emails)
finally:
    exporter.closeConnection()
    fetcher.end()
