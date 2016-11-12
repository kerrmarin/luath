import imaplib, email, email.header

class GmailFetcher():

    def __init__(self):
        """
        Connects to Google's imap mailbox via SSL
        """
        self.mailbox = imaplib.IMAP4_SSL('imap.gmail.com')

    def login(self, username, password):
        """
        Logins to the given mailbox using the given credentials
        Returns True is login was successful, false otherwise
        """
        try:
            self.mailbox.login(username, password)
        except imaplib.IMAP4.error as e:
            print e
            return False
        return True

    def selectFolder(self, folder):
        """
        Selects a mailbox folder.
        Returns True if the selection was successful, false otherwise
        """
        returnvalue, data = self.mailbox.select(folder)
        if returnvalue == 'OK':
            return True
        else:
            return False

    def __getUnseenEmails(self):
        """
        Returns the unseen emails from a mailbox, or an empty array if there was
        an error
        """
        returnvalue, data = self.mailbox.search(None, "(UNSEEN)")
        if returnvalue != 'OK':
            return []
        return data

    def __getEmailAtIndex(self, index):
        """
        Retrieves the email from the mailbox at a given index.
        Must have selected a folder before this occurs.
        """
        returnvalue, data = self.mailbox.fetch(index, '(RFC822)')
        if returnvalue != 'OK':
            return None
        return email.message_from_string(data[0][1])

    def fetchEmails(self):
        """
        Gets all unseen emails from a given mailbox, parses them into email.message
        types and returns them
        """
        emails = []
        data = self.__getUnseenEmails()
        for index in data[0].split():
            message = self.__getEmailAtIndex(index)
            if not message:
                print "Couldn't get message at index:", index
                continue
            emails.append(message)
        return emails

    def end(self):
        self.mailbox.close()
        self.mailbox.logout()
