import email, re
from Email import Email

class EmailConverter:

    def convertEmailsFromMessages(self, messages):
        emails = []
        for message in messages:
            messageid = self.getMessageIdFromMessageHeader(message)
            fromEmail = self.getEmailFromMessageHeader(message)
            fromName = self.getNameFromMessageHeader(message)
            inreply = self.getInReplyToFromMessageHeader(message)
            date = message.get("Date")
            subject = message.get("Subject")
            references = self.getReferencesFromMessageHeader(message)
            content = self.getMessagePayload(message)
            listnames = self.getListsFromSubject(subject)
            normalised = Email(messageid, fromEmail, fromName,
                inreply, date, subject, content, listnames, references)
            emails.append(normalised)
        return emails

    def getListsFromSubject(self, subject):
        regex = r'\[(.+?)\]'
        matches = re.findall(regex, subject)
        return matches

    def getNameFromMessageHeader(self, message):
        components = self.getComponentsFromMessageHeader(message)
        return components[1]

    def getEmailFromMessageHeader(self, message):
        components = self.getComponentsFromMessageHeader(message)
        return components[0]

    def getComponentsFromMessageHeader(self, message):
        fromHeader = message.get("From")
        regex = r'(\S+) at (\S+) \((.+)\)'
        match = re.match(regex, fromHeader)
        email = "%s@%s" % (match.groups()[0], match.groups()[1])
        return (email, match.groups()[2])

    def getInReplyToFromMessageHeader(self, message):
        inreplytoheader = message.get("In-Reply-To")
        if not inreplytoheader:
            return None
        regex = r'<(.+)>'
        match = re.match(regex, inreplytoheader)
        if match:
            return match.groups()[0]
        return None

    def getReferencesFromMessageHeader(self, message):
        referencesHeader = message.get("References")
        if not referencesHeader:
            return []
        regex = r'<(.+?)>'
        matches = re.findall(regex, referencesHeader)
        return matches

    def getMessageIdFromMessageHeader(self, message):
        messageIdHeader = message.get("Message-ID")
        regex = r'<(.+)>'
        match = re.match(regex, messageIdHeader)
        return match.groups()[0]

    def getMessagePayload(self, message):
        content = ""
        for part in message.walk():
            if part.get_content_type() == "text/plain": # ignore attachments/html
                body = part.get_payload(decode=True)
                content += body.decode('utf-8')
            else:
                continue
            return content
