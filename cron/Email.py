from email.utils import parsedate
from datetime import datetime
import time

class Email:
    def __init__(self, messageid, fromEmail, fromName, inreplyto,
    date, subject, content, listnames, references):
        self.messageid = messageid
        self.fromEmail = fromEmail
        self.fromName = fromName
        self.dateString = date
        self.inreplyto = inreplyto
        self.date = datetime.fromtimestamp(time.mktime(parsedate(date)))
        self.subject = info = (subject[:298] + '..') if len(subject) > 300 else subject
        self.content = content
        self.listnames = listnames
        self.references = set(references)

    def __str__(self):
        return "<%s> - From: %s (%s) \n \
        List: %s - subject: %s, date: %s" % (self.messageid, self.fromName,
        self.fromEmail, self.listnames, self.subject, self.dateString)
