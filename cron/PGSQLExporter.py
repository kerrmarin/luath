
import psycopg2
from datetime import datetime
import sys

class PGSQLConfiguration:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

class PGSQLExporter:

    def __init__(self, configuration):
        self.configuration = configuration
        connectionString = "dbname=%s user=%s" % (configuration.database, configuration.user)
        self.connection = psycopg2.connect(connectionString)

    def export(self, emails):
        try:
            with self.connection.cursor() as cursor:
                select_message_id = "SELECT message_id FROM luath_api_message WHERE message_id=%s"
                insert_message_list = "INSERT INTO luath_api_message_lists (message_id, list_id) VALUES (%s, %s)"
                select_list_id = "SELECT list_id FROM luath_api_list WHERE list_name=%s"
                insert_message = "INSERT INTO luath_api_message (message_id, from_email, from_name, date, in_reply_to, subject, content) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                for email in emails:
                    tableContainsEmail = self.__containsEmail(cursor, select_message_id, email)
                    if tableContainsEmail:
                        continue

                    self.__insertEmail(cursor, insert_message, email)

                    for listname in email.listnames:
                        listid = self.__getListIdFromName(cursor, select_list_id, listname)
                        if not listid:
                            continue
                        cursor.execute(insert_message_list, (email.messageid, listid[0],))

                self.connection.commit()
                cursor.close()
        except Exception as e:
            self.__handleError(e)

    def addReferences(self, emails):
        try:
            with self.connection.cursor() as cursor:
                insert_reference = "INSERT INTO luath_api_message_references (from_message_id, to_message_id) VALUES (%s, %s)"

                for email in emails:
                    for reference in email.references:
                        cursor.execute(insert_reference, (email.messageid, reference,))

                self.connection.commit()
                cursor.close()
        except Exception as e:
            self.__handleError(e)

    def closeConnection(self):
        self.connection.close()

    def __insertEmail(self, cursor, sql, email):
        cursor.execute(sql, (
            email.messageid,
            email.fromEmail,
            email.fromName,
            datetime.now(),
            email.inreplyto,
            email.subject,
            email.content)
        )

    def __containsEmail(self, cursor, sql, email):
        cursor.execute(sql, (email.messageid,))
        messageid = cursor.fetchone()
        return messageid != None

    def __getListIdFromName(self, cursor, sql, listname):
        cursor.execute(sql, (listname,))
        return cursor.fetchone()

    def __handleError(self, error):
        print('Got error {!r}, errno is {}'.format(error, error.args[0]))
