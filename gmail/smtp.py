import time
from smtplib import SMTP
from email.utils import make_msgid, formatdate


GMAIL_SMTP_HOST = 'smtp.gmail.com'
GMAIL_SMTP_PORT = 587


class GSMTP(object):

    def __init__(self, username, password):

        self.sender = username
        self.sess = SMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT)
        self.sess.ehlo()
        self.sess.starttls()
        self.sess.ehlo()
        self.sess.login(username, password)


    def send(self, rcpt, body):

        message = '\n'.join([
            'From: {}'.format(self.sender),
            'Reply-To: {}'.format(self.sender),
            'To: {}'.format(rcpt),
            'Date: {}'.format(formatdate(time.time())),
            'Message-ID: {}'.format(make_msgid()),
            'Subject: ',
            '', body, '',
            ])

        self.sess.sendmail(self.sender, rcpt, message)
