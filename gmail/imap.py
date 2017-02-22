from imaplib import IMAP4_SSL
from email import message_from_string


GMAIL_IMAP_HOST = 'imap.gmail.com'
GMAIL_IMAP_PORT = 993


class GIMAP(object):

    def __init__(self, username, password):

        self.imap = IMAP4_SSL(GMAIL_IMAP_HOST, GMAIL_IMAP_PORT)
        code, _ = self.imap.login(username, password)
        if code != 'OK':
            raise Exception('gmail login failure')
        self.imap.select('INBOX')


    def search(self, query):

        # TODO check sanatization
        code, data = self.imap.uid('SEARCH', None, r'(X-GM-RAW "{}")'.format(query.replace('"', r'\"')))
        if code != 'OK':
            raise Exception('gmail search failure')
        return list(map(int, filter(None, data[0].decode('utf-8').split(' '))))


    def fetch(self, uid):

        code, data = self.imap.uid('FETCH', str(uid), 'BODY.PEEK[]') # '(BODY.PEEK[] X-GM-THRID X-GM-MSGID)'
        if code != 'OK':
            raise Exception('gmail fetch failure')
        return message_from_string(data[0][1].decode('utf-8'))
