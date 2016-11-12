
import re, email, os, gzip

class EmailParser:

    delimiterRegex = r'(From .+ at .+  (?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) .{3}  ?\d{1,2} \d{2}:\d{2}:\d{2} \d{4})'

    def parse(self, filepath):
        email_messages = []
        with gzip.open(filepath, 'rb') as f:
            try:
                lines = f.read()
            except:
                return []

            splitEmails = re.split(self.delimiterRegex, lines)
            emailTuples = zip(splitEmails[1::2], splitEmails[2::2])

            for emailTuple in emailTuples:
                m = emailTuple[0] + emailTuple[1]
                message = email.message_from_string(m)
                email_messages.append(message)
        return email_messages
