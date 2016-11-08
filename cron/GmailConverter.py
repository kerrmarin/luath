import email, re, os, sys
from Email import Email
from EmailConverter import EmailConverter

class GmailConverter(EmailConverter):

    def getComponentsFromMessageHeader(self, message):
        fromHeader = message.get("Reply-To")
        regex = r'(.+) <(.+?)>'
        match = re.match(regex, fromHeader)
        email = "%s@%s" % (match.groups()[0], match.groups()[1])
        return (match.groups()[1], match.groups()[0])
